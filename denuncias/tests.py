from pathlib import Path

from django.test import SimpleTestCase
from django.urls import NoReverseMatch, reverse


class DenunciaEstadoPublicoTests(SimpleTestCase):
    templates_dir = Path(__file__).resolve().parent / "templates"

    def test_no_existe_ruta_publica_para_editar_estado(self):
        with self.assertRaises(NoReverseMatch):
            reverse("editar_estado", args=[1])

    def test_listado_no_muestra_accion_editar_estado(self):
        template = (self.templates_dir / "lista.html").read_text(encoding="utf-8")

        self.assertNotIn("Editar estado", template)
        self.assertNotIn("editar-estado", template)
        self.assertNotIn("editar_estado", template)

    def test_detalle_no_muestra_accion_editar_estado(self):
        template = (self.templates_dir / "detalle_denuncia.html").read_text(encoding="utf-8")

        self.assertNotIn("Editar estado", template)
        self.assertNotIn("editar-estado", template)
        self.assertNotIn("editar_estado", template)

    def test_mis_denuncias_no_muestra_accion_editar_estado(self):
        template = (self.templates_dir / "mis_denuncias.html").read_text(encoding="utf-8")

        self.assertNotIn("Editar estado", template)
        self.assertNotIn("editar-estado", template)
        self.assertNotIn("editar_estado", template)
