import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import requests
from PIL import Image, ImageChops, ImageSequence
from assets import assets
from github_activity import GitHubClient
from repo_profile import DirectoryProfile, profile_repository
from layout import DIRECTIONS, build_layout
from renderer import save_world


def repository(name='example', count=6):
    return {'name': name, 'main_language': 'Python', 'languages': {'Python': 100, 'JavaScript': 30},
            'topics': ['research'], 'tree': [{'path': f'dir{d}/nested/file{f}.py', 'type': 'blob'}
                                          for d in range(count) for f in range(d*25+1)],
            'as_of': '2026-09-30T00:00:00Z', 'pushed_at': '2026-05-01T00:00:00Z', 'recent_commits': 20}


class ProfileTests(unittest.TestCase):
    def test_grouping_keeps_all_files_and_detects_features(self):
        data = repository(count=8)
        data['tree'] += [{'path': p, 'type': 'blob'} for p in ['README.md', 'tests/test_world.py', 'package.json']]
        p = profile_repository(data)
        self.assertEqual(len(p.districts), 6)
        self.assertEqual(sum(d.files for d in p.districts), p.files)
        self.assertEqual(p.max_depth, 2)
        self.assertTrue(p.has_tests and p.has_docs)
        self.assertEqual(p.dependencies, 1)
        self.assertEqual(p.theme, 'research')
        self.assertGreater(p.days_inactive, 90)
        self.assertEqual([DirectoryProfile('d', n, 1).size for n in [1, 20, 80]], [1, 2, 3])

    def test_empty_and_truncated_repository(self):
        p = profile_repository({'name': 'empty', 'tree_truncated': True})
        self.assertTrue(p.incomplete)
        self.assertEqual(p.files, 0)
        self.assertEqual(len(p.districts), 1)
        self.assertIsNone(p.recent_commits)

    def test_layout_does_not_overlap_objects_or_paths(self):
        profiles = [profile_repository(repository(str(n),n)) for n in [1,3,8]]
        islands, dimensions = build_layout(profiles)
        for island in islands:
            used = set()
            for name,x,y in island.objects:
                tile = assets.get(name)
                footprint = {(a,b) for a in range(x,x+tile.width) for b in range(y,y+tile.height)}
                self.assertFalse(used & footprint)
                self.assertFalse(island.paths & footprint)
                used.update(footprint)
                self.assertLess(x+tile.width, dimensions[0])
                self.assertLess(y+tile.height, dimensions[1])
            self.assertEqual(len(island.districts),min(3,len(island.profile.districts)))
            self.assertEqual(sum(d.files for d,x,y in island.districts),island.profile.files)
            self.assertTrue(island.paths <= island.ground)
            self.assertTrue(island.occupied <= island.ground)

    def test_modules_share_sides_and_paths_connect_all_anchors(self):
        data = repository(count=8)
        data['tree'] += [{'path': path, 'type': 'blob'} for path in ['tests/test_x.py', 'README.md', 'package.json']]
        island = build_layout([profile_repository(data)])[0][0]
        modules = {(m.q, m.r): m for m in island.modules}
        self.assertEqual({m.kind for m in island.modules}, {'plaza', 'house', 'garden'})
        for module in island.modules[1:]:
            parent = modules[module.parent]
            self.assertIn((module.q-parent.q, module.r-parent.r), DIRECTIONS)
            self.assertFalse(module.cells & parent.cells)
            self.assertTrue(any((x+dx,y+dy) in parent.cells for x,y in module.cells for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))))
        reached = set()
        pending = [island.modules[0].anchor]
        while pending:
            point = pending.pop()
            if point in reached:
                continue
            reached.add(point)
            x,y = point
            pending.extend(p for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if p in island.paths and p not in reached)
        self.assertEqual(reached,island.paths)
        self.assertTrue({m.anchor for m in island.modules} <= reached)
        self.assertIn(island.entrance,reached)
        self.assertIn(island.exit,reached)

    def test_file_growth_preserves_module_coordinates(self):
        data = repository(count=3)
        before = build_layout([profile_repository(data)])[0][0]
        data['tree'] += [{'path': f'dir0/nested/extra{n}.py', 'type': 'blob'} for n in range(100)]
        after = build_layout([profile_repository(data)])[0][0]
        self.assertEqual({m.key: (m.q,m.r) for m in before.modules}, {m.key: (m.q,m.r) for m in after.modules})
        self.assertNotEqual([name for name,x,y in before.objects if name.startswith('cv')], [name for name,x,y in after.objects if name.startswith('cv')])

    def test_identical_data_produces_identical_outputs(self):
        p = profile_repository(repository())
        with tempfile.TemporaryDirectory() as root:
            for name in ['first','second']:
                islands, dimensions = build_layout([p])
                save_world(islands,dimensions,Path(root)/name)
            for name in ['map.png','world.gif']:
                first = (Path(root)/'first'/name).read_bytes()
                second = (Path(root)/'second'/name).read_bytes()
                self.assertEqual(hashlib.sha256(first).digest(),hashlib.sha256(second).digest())

    def test_transparent_png_and_every_gif_frame(self):
        islands, dimensions = build_layout([profile_repository(repository())])
        self.assertLessEqual(len(islands[0].modules),5)
        with tempfile.TemporaryDirectory() as root:
            save_world(islands,dimensions,root)
            with Image.open(Path(root)/'map.png') as png:
                self.assertEqual(png.getpixel((0,0))[3],0)
                png_alpha = png.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
            with Image.open(Path(root)/'world.gif') as gif:
                self.assertEqual(gif.info['transparency'],255)
                self.assertGreater(gif.n_frames,1)
                menu_bounds = []
                for frame in ImageSequence.Iterator(gif):
                    rgba = frame.convert('RGBA')
                    self.assertEqual(rgba.getpixel((0,0))[3],0)
                    frame_alpha = rgba.getchannel('A')
                    # O mapa continua visível por inteiro; o painel acrescenta pixels
                    # opacos somente na área reservada ao personagem.
                    self.assertIsNone(ImageChops.subtract(png_alpha,frame_alpha).getbbox())
                    menu_bounds.append(ImageChops.difference(frame_alpha,png_alpha).getbbox())
                self.assertTrue(all(bounds is not None for bounds in menu_bounds))

    def test_all_asset_crops_fit_their_source(self):
        for name in assets.list():
            tile = assets.get(name)
            self.assertLessEqual((tile.col+tile.width)*tile.tile_size,tile.tileset.width,name)
            self.assertLessEqual((tile.row+tile.height)*tile.tile_size,tile.tileset.height,name)


class CollectionTests(unittest.TestCase):
    def test_optional_api_failure_is_marked_as_unknown(self):
        repo = {'name': 'empty', 'full_name': 'user/empty', 'default_branch': 'main'}
        client = GitHubClient()
        with patch.object(client,'repositories',return_value=[repo]), patch.object(client,'get',side_effect=requests.HTTPError('403')):
            data = client.collect()[0]
        self.assertTrue(data['tree_unavailable'])
        self.assertIsNone(data['recent_commits'])
        self.assertEqual(len(data['warnings']),3)

    def test_forks_do_not_reduce_requested_count(self):
        client = GitHubClient()
        page1 = [{'name': str(n), 'fork': True} for n in range(100)]
        page2 = [{'name': 'own', 'fork': False}]
        with patch.object(client,'get',side_effect=[page1,page2]) as get:
            self.assertEqual(client.repositories('user',3),page2)
        self.assertEqual(get.call_count,2)


if __name__ == '__main__':
    unittest.main()
