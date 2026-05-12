from pathlib import Path

from django.test import SimpleTestCase
from django.urls import NoReverseMatch, reverse

from ia.classificador import analizar_denuncia

from .admin import ClasificacionIAInline, DenunciaAdmin, GeolocalizacionInline, SeguimientoInline
from .models import ClasificacionIA, Denuncia, ESTADOS_DENUNCIA, Seguimiento


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

    def test_listado_publico_no_expone_datos_sensibles(self):
        template = (self.templates_dir / "lista.html").read_text(encoding="utf-8")

        self.assertNotIn("denuncia.usuario", template)
        self.assertNotIn("geolocalizacion", template)
        self.assertIn("Descripcion resumida", template)
        self.assertIn("Iniciar sesion", template)

    def test_detalle_requiere_inicio_de_sesion(self):
        response = self.client.get(reverse("detalle_denuncia", args=[1]))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
        self.assertIn("next=/denuncias/1/", response["Location"])

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

    def test_login_conserva_siguiente_url(self):
        template = (self.templates_dir / "login.html").read_text(encoding="utf-8")

        self.assertIn('name="next"', template)

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
        self.assertIn(ClasificacionIAInline, DenunciaAdmin.inlines)
        self.assertIn(GeolocalizacionInline, DenunciaAdmin.inlines)
        self.assertIn(SeguimientoInline, DenunciaAdmin.inlines)
        self.assertIn("enlace_mapa", DenunciaAdmin.readonly_fields)

    def test_clasificacion_ia_guarda_validez_y_motivo(self):
        self.assertIsNotNone(ClasificacionIA._meta.get_field("validez"))
        self.assertIsNotNone(ClasificacionIA._meta.get_field("motivo"))


class ClasificadorIATests(SimpleTestCase):
    def test_clasifica_denuncia_valida_por_palabras_clave(self):
        resultado = analizar_denuncia(
            "Hueco peligroso en la via",
            "Hay un hueco grande en la calle principal que afecta el paso de vehiculos.",
        )

        self.assertEqual(resultado["categoria_predicha"], "Infraestructura")
        self.assertEqual(resultado["validez"], "Valida")
        self.assertGreaterEqual(resultado["confianza"], 0.45)

    def test_marca_reporte_corto_como_posiblemente_invalido(self):
        resultado = analizar_denuncia("Prueba", "asdf")

        self.assertEqual(resultado["validez"], "Posiblemente invalida")


class HomeCategoriasTests(SimpleTestCase):
    templates_dir = Path(__file__).resolve().parent / "templates"

    def test_home_muestra_entidad_y_descripcion_por_categoria(self):
        template = (self.templates_dir / "home.html").read_text(encoding="utf-8")

        self.assertIn("categoria.entidad", template)
        self.assertIn("categoria.descripcion", template)
