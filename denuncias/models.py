from django.db import models


ESTADO_PENDIENTE = "Pendiente"
ESTADO_EN_PROCESO = "En Proceso"
ESTADO_RESUELTA = "Resuelta"

ESTADOS_DENUNCIA = [
    (ESTADO_PENDIENTE, "Pendiente"),
    (ESTADO_EN_PROCESO, "En Proceso"),
    (ESTADO_RESUELTA, "Resuelta"),
]


class Usuario(models.Model):
    id = models.AutoField(db_column='UsuarioID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    apellido = models.CharField(db_column='Apellido', max_length=100)
    email = models.EmailField(db_column='Email', unique=True, max_length=150)
    password_hash = models.CharField(db_column='PasswordHash', max_length=255)
    rol = models.CharField(db_column='Rol', max_length=50)
    fecha_registro = models.DateTimeField(db_column='FechaRegistro', auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

    class Meta:
        db_table = 'Usuarios'
        managed = True


class Categoria(models.Model):
    id = models.AutoField(db_column='CategoriaID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre  # CLAVE

    class Meta:
        db_table = 'Categorias'
        managed = True


class Denuncia(models.Model):
    id = models.AutoField(db_column='DenunciaID', primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='UsuarioID')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, db_column='CategoriaID')
    titulo = models.CharField(db_column='Titulo', max_length=200)
    descripcion = models.TextField(db_column='Descripcion')
    imagen = models.ImageField(db_column='Imagen', upload_to='denuncias/', null=True, blank=True)
    estado = models.CharField(
        db_column='Estado',
        max_length=50,
        choices=ESTADOS_DENUNCIA,
        default=ESTADO_PENDIENTE,
    )
    fecha_registro = models.DateTimeField(db_column='FechaRegistro', auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'Denuncias'
        managed = True


class Geolocalizacion(models.Model):
    id = models.AutoField(db_column='GeoID', primary_key=True)
    denuncia = models.OneToOneField(Denuncia, on_delete=models.CASCADE, db_column='DenunciaID')
    latitud = models.DecimalField(db_column='Latitud', max_digits=9, decimal_places=6)
    longitud = models.DecimalField(db_column='Longitud', max_digits=9, decimal_places=6)
    direccion = models.CharField(db_column='Direccion', max_length=255)

    def __str__(self):
        return f"{self.denuncia} - {self.direccion}"

    class Meta:
        db_table = 'Geolocalizacion'
        managed = True


class Seguimiento(models.Model):
    id = models.AutoField(db_column='SeguimientoID', primary_key=True)
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, db_column='DenunciaID')
    funcionario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='FuncionarioID')
    comentario = models.CharField(db_column='Comentario', max_length=500)
    estado = models.CharField(db_column='Estado', max_length=50, choices=ESTADOS_DENUNCIA)
    fecha = models.DateTimeField(db_column='Fecha', auto_now_add=True)

    def __str__(self):
        return f"{self.denuncia} - {self.estado}"

    class Meta:
        db_table = 'Seguimiento'
        managed = True


class ClasificacionIA(models.Model):
    id = models.AutoField(db_column='ClasificacionID', primary_key=True)
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, db_column='DenunciaID')
    categoria_predicha = models.CharField(db_column='CategoriaPredicha', max_length=100)
    confianza = models.FloatField(db_column='Confianza')
    validez = models.CharField(db_column='Validez', max_length=50, default='Requiere revision')
    motivo = models.CharField(db_column='Motivo', max_length=255, null=True, blank=True)
    fecha = models.DateTimeField(db_column='Fecha', auto_now_add=True)

    def __str__(self):
        return f"{self.denuncia} - {self.categoria_predicha} ({self.validez})"

    class Meta:
        db_table = 'ClasificacionIA'
        managed = True
