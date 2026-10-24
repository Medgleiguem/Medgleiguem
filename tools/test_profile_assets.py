"""Verify the SVG image boundary: local bitmap artwork, no remote or active content."""
import base64
import unittest
import verify_profile
import generate_assets
import xml.etree.ElementTree as ET
from pathlib import Path
import tempfile


class SVGImageBoundaryTests(unittest.TestCase):
    def validate(self, body):
        self.assertTrue(hasattr(verify_profile, 'validate_svg'), 'SVG bitmap validation is not implemented')
        return verify_profile.validate_svg('<svg xmlns="http://www.w3.org/2000/svg">'+body+'</svg>')

    def test_embedded_jpeg_artwork_is_allowed(self):
        jpeg=base64.b64encode(b'\xff\xd8\xff\xe0image bytes').decode()
        self.validate('<image href="data:image/jpeg;base64,'+jpeg+'"/>')

    def test_remote_image_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'bitmap'):
            self.validate('<image href="https://example.com/tracking.jpg"/>')

    def test_embedded_svg_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'bitmap'):
            self.validate('<image href="data:image/svg+xml;base64,PHN2Zy8+"/>')

    def test_event_handler_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'executable'):
            self.validate('<rect width="20" height="20" onload="alert(1)"/>')

    def test_static_render_preserves_markup_with_inline_animation_delays(self):
        source='<svg xmlns="http://www.w3.org/2000/svg"><style>@keyframes move{to{opacity:.5}}.icon{animation:move 2s infinite}</style><g style="animation-delay:-2s"><text>Keep this label</text></g></svg>'
        try:
            root=ET.fromstring(generate_assets.static_svg(source))
        except ET.ParseError:
            self.fail('Static rendering damaged valid SVG markup')
        self.assertEqual(root.find('.//{http://www.w3.org/2000/svg}text').text,'Keep this label')
        self.assertNotIn('animation-delay',ET.tostring(root,encoding='unicode'))

    def test_static_render_removes_native_svg_motion_without_losing_art(self):
        source = '<svg xmlns="http://www.w3.org/2000/svg"><title>Signal</title><g><circle cx="10" cy="10" r="3" opacity=".7"><animate attributeName="opacity" values=".2;1;.2" dur="8s" repeatCount="indefinite"/></circle><path d="M0 0H20"><animateMotion dur="5s" path="M0 0H10"/></path></g></svg>'
        root = ET.fromstring(generate_assets.static_svg(source))
        tags = [node.tag.rsplit('}', 1)[-1] for node in root.iter()]
        self.assertNotIn('animate', tags)
        self.assertNotIn('animateMotion', tags)
        self.assertIn('circle', tags)
        self.assertIn('path', tags)
        self.assertEqual(root.find('.//{http://www.w3.org/2000/svg}circle').get('opacity'), '.7')

    def test_local_briefs_are_checked_without_treating_external_links_as_files(self):
        self.assertTrue(hasattr(verify_profile, 'validate_local_links'), 'Local brief validation is missing')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'brief.md').write_text('# A real brief')
            verify_profile.validate_local_links('[Brief](./brief.md#method) [Mail](mailto:me@example.com) [GitHub](https://github.com) [Section](#research)', root, root)
            with self.assertRaisesRegex(AssertionError, 'Missing local'):
                verify_profile.validate_local_links('[Brief](./missing.md)', root, root)

    def test_public_links_cannot_escape_the_repository(self):
        self.assertTrue(hasattr(verify_profile, 'validate_local_links'), 'Local brief validation is missing')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'repo').mkdir()
            (root/'unpublished.md').write_text('Not in the public repository')
            with self.assertRaisesRegex(AssertionError, 'outside'):
                verify_profile.validate_local_links('<a href="../unpublished.md">Broken public brief</a>', root/'repo', root/'repo')

    def test_profile_navigation_matches_github_sanitized_anchor_ids(self):
        self.assertTrue(hasattr(verify_profile, 'validate_profile_navigation'), 'GitHub navigation validation is missing')
        with self.assertRaisesRegex(AssertionError, 'navigation'):
            verify_profile.validate_profile_navigation('<a id="research"></a> [Research](#research)')
        verify_profile.validate_profile_navigation('<a id="research"></a> [Research](#user-content-research)')
        verify_profile.validate_profile_navigation((Path(__file__).resolve().parents[1]/'README.md').read_text())


if __name__=='__main__':unittest.main()
