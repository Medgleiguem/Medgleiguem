"""Verify the SVG image boundary: local bitmap artwork, no remote or active content."""
import base64
import unittest
import verify_profile


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


if __name__=='__main__':unittest.main()
