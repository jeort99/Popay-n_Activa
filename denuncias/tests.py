from pathlib import Path

from django.test import SimpleTestCase
from django.urls import NoReverseMatch, reverse

from .admin import DenunciaAdmin, GeolocalizacionInline, SeguimientoInline
from .models import Denuncia, ESTADOS_DENUNCIA, Seguimiento


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


class AutenticacionCiudadanaTests(SimpleTestCase):
    templates_dir = Path(__file__).resolve().parent / "templates"

    def test_rutas_de_autenticacion_estan_disponibles(self):
        self.assertEqual(reverse("registro"), "/registro/")
        self.assertEqual(reverse("login"), "/login/")
        self.assertEqual(reverse("logout"), "/logout/")

    def test_formulario_denuncia_no_pide_datos_del_ciudadano(self):
        template = (self.templates_dir / "registrar_denuncia.html").read_text(encoding="utf-8")

        self.assertNotIn("form.nombre", template)
        self.assertNotIn("form.apellido", template)
        self.assertNotIn("form.email", template)

    def test_formulario_denuncia_incluye_geolocalizacion(self):
        template = (self.templates_dir / "registrar_denuncia.html").read_text(encoding="utf-8")

        self.assertIn("form.latitud", template)
        self.assertIn("form.longitud", template)
        self.assertIn("geo-button", template)
        self.assertIn("navigator.geolocation", template)


class AdministradorTests(SimpleTestCase):
    def test_estados_estan_controlados_en_modelos_principales(self):
        self.assertEqual(Denuncia._meta.get_field("estado").choices, ESTADOS_DENUNCIA)
        self.assertEqual(Seguimiento._meta.get_field("estado").choices, ESTADOS_DENUNCIA)

    def test_denuncia_admin_tiene_flujo_de_gestion(self):
        self.assertIn("marcar_pendiente", DenunciaAdmin.actions)
        self.assertIn("marcar_en_proceso", DenunciaAdmin.actions)
        self.assertIn("marcar_resuelta", DenunciaAdmin.actions)
        self.assertIn(GeolocalizacionInline, DenunciaAdmin.inlines)
        self.assertIn(SeguimientoInline, DenunciaAdmin.inlines)
        self.assertIn("enlace_mapa", DenunciaAdmin.readonly_fields)
