from django.shortcuts import render, redirect
from .models import User, Pub, Follow, PubComentario, PubLike

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        informacion = User.objects.filter(username=request.POST['username'], password=request.POST['password']).exists()

        if informacion is True:
            obtener = User.objects.get(username=request.POST['username'], password=request.POST['password'])
            request.session['login'] = 1
            request.session['user_id'] = obtener.id
            
            return redirect('noticias')
        else:
            return render(request, 'home.html', {'error' : 'Credenciales invalidas'})
    else:
        if(request.session.get('login') == 1):
            return redirect('noticias')
        else:
            return render(request, 'home.html')
            
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        usuario = User.objects.filter(username=request.POST['username']).exists()
        if usuario is True:
            return render(request, 'registro.html', {'error' : 'El usuario ya existe.'})
        else:
            correo = User.objects.filter(email=request.POST['correo']).exists()
            if correo is True:
                return render(request, 'registro.html', {'error' : 'El correo ya existe.'})
            else:
                crear = User.objects.create(username=request.POST['username'], email=request.POST['correo'], nombre=request.POST['nombre'], password=request.POST['password'])
                request.session['login'] = 1
                request.session['user_id'] = crear.id
                
                return redirect('noticias')
    else:
        if(request.session.get('login') == 1):
            return redirect('noticias')
        else:
            return render(request, 'registro.html')

    return render(request, 'registro.html')

def noticias(request):
    if request.method == 'GET':
        if(request.session.get('login') != 1):
            return redirect('home')
        else:
            publicacion = []
            comentario = []
            likes = []
            seguidores = Follow.objects.all().filter(id_usuario=request.session['user_id'])
            for seguidor in seguidores:
                publicacion.append(seguidor.id_usuario_seguido.id)
            
            publicacion.append(request.session['user_id'])
            publicaciones = Pub.objects.all().filter(id_usuario__in=publicacion).order_by('-fecha')
            
            for publicar in publicaciones:
                cant = PubLike.objects.filter(id_publicacion=publicar.id).count()
                likes.append([publicar.id, cant])
            
                comentarios = PubComentario.objects.all().filter(id_publicacion=publicar.id)
                for comentar in comentarios:
                    comentario.append([comentar.id, publicar.id, comentar.id_usuario.username, comentar.mensaje, comentar.id_usuario.id])
            
            return render(request, 'noticias.html', {'publicaciones':publicaciones, 'cantidad':likes, 'comentario':comentario})
            
    return render(request, 'noticias.html')

def perfil(request):
    if request.method == 'GET':
        publicaciones = Pub.objects.filter(id_usuario=request.session['user_id'])
        usuarios = User.objects.filter(id=request.session['user_id'])
        total_publicaciones = Pub.objects.filter(id_usuario=request.session['user_id']).count()
        total_seguidos = Follow.objects.filter(id_usuario=request.session['user_id']).count()
        total_seguidores = Follow.objects.filter(id_usuario_seguido=request.session['user_id']).count()
        
        return render(request, 'perfil.html', {'publicaciones':publicaciones, 'usuarios':usuarios, 'total_publicaciones':total_publicaciones, 'total_seguidos':total_seguidos, 'total_seguidores':total_seguidores})
    else:
        try:
            usuario = User.objects.get(username=request.POST['search'])
            
            publicaciones = Pub.objects.filter(id_usuario=usuario.id)
            usuarios = User.objects.filter(id=usuario.id)
            total_publicaciones = Pub.objects.filter(id_usuario=usuario.id).count()
            total_seguidos = Follow.objects.filter(id_usuario=usuario.id).count()
            total_seguidores = Follow.objects.filter(id_usuario_seguido=usuario.id).count()
            
            try:
                seguidor = Follow.objects.get(id_usuario=request.session['user_id'], id_usuario_seguido=usuario.id)
                
                return render(request, 'perfil.html', {'publicaciones':publicaciones, 'usuarios':usuarios, 'total_publicaciones':total_publicaciones, 'total_seguidos':total_seguidos, 'total_seguidores':total_seguidores, 'seguidor':seguidor})
            except Follow.DoesNotExist:
                return render(request, 'perfil.html', {'publicaciones':publicaciones, 'usuarios':usuarios, 'total_publicaciones':total_publicaciones, 'total_seguidos':total_seguidos, 'total_seguidores':total_seguidores, 'seguidor':''})
        except User.DoesNotExist:
            return redirect('noticias')

def agregar_publicacion(request):
    if request.method == 'POST':
        usuario = User.objects.get(pk = request.session['user_id'])
        publicacion = Pub.objects.create(id_usuario=usuario, imagen=request.FILES['imagen'], mensaje=request.POST['mensaje'])
        
        return redirect('perfil')
        
def editar_perfil(request):
    if request.method == 'POST':
        usuario = User.objects.get(id = request.session['user_id'])
        usuario.nombre = request.POST['nombre']
        usuario.save()
        
        return redirect('perfil')

def seguir_perfil(request):
    if request.method == 'POST':
        usuario = User.objects.get(pk = request.session['user_id'])
        seguidor = User.objects.get(pk = request.POST['usuario'])
        
        if request.POST['opcion'] == 'Seguir':
            seguir = Follow.objects.create(id_usuario=usuario, id_usuario_seguido=seguidor)
        else:
            dejar_seguir = Follow.objects.get(id_usuario=usuario, id_usuario_seguido=seguidor)
            dejar_seguir.delete()
        
        return redirect('noticias')
        
def comentar(request):
    if request.method == 'POST':
        publicacion = Pub.objects.get(pk = request.POST['publicacion'])
        usuario = User.objects.get(pk = request.session['user_id'])
        
        comentar = PubComentario.objects.create(id_publicacion=publicacion, id_usuario=usuario, mensaje=request.POST['comentario'])
        return redirect('noticias')

def me_gusta(request):
    if request.method == 'POST':
        publicacion = Pub.objects.get(pk = request.POST['publicacion'])
        usuario = User.objects.get(pk = request.session['user_id'])
        verificar = PubLike.objects.filter(id_publicacion=publicacion, id_usuario=usuario).count()
        
        if verificar > 0:
            eliminar = PubLike.objects.filter(id_publicacion=publicacion, id_usuario=usuario)
            eliminar.delete()
        else:
            crear = PubLike.objects.create(id_publicacion=publicacion, id_usuario=usuario)
    
        return redirect('noticias')
        
def borrar_publicacion(request):
    if request.method == 'POST':
        publicacion = Pub.objects.get(pk = request.POST['publicacion'])
        
        eliminar = Pub.objects.filter(id=publicacion.id)
        eliminar.delete()
        return redirect('noticias')

def borrar_comentario(request):
    if request.method == 'POST':
        comentario = PubComentario.objects.get(pk = request.POST['id'])
        
        eliminar = PubComentario.objects.filter(id=comentario.id)
        eliminar.delete()
        return redirect('noticias')

def logout(request):
    del request.session['login']
    del request.session['user_id']
    return render(request, 'home.html')