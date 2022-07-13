from flask  import Flask,jsonify, request
from flask_restful import Api
import basicauth

app=Flask(__name__)

from usuarios import usuarios

# Get Data Rutas
@app.route('/usuarios',methods=['GET'])
def getListUsuarios():
    # return jsonify({'usuarios': usuarios}),200
    return jsonify({"message": "Lista de usuarios","usuarios":usuarios}),200


@app.route('/usuarios/<int:usuario_id>')
def getUsuario(usuario_id):
    usuariosFound = [
        usuario for usuario in usuarios if usuarios['id'] == usuario_id.lower()]
    if (len(usuariosFound) > 0):
        return jsonify({'usuario': usuariosFound[0]})
    return jsonify({'message': 'Usuario no encontrado'})


    
@app.route('/usuario/<name>', methods=['GET'])
def getLoginUser(name):
    header = request.headers
    authorization = header.get('Authorization')
    if (authorization) is None:
        return jsonify({'message': 'Se requiere Usuario y Contraseña'}), 401
    
    if ("Basic " in authorization):
        username, passwd = basicauth.decode(authorization)

        if (username) == 'gabriela' and (passwd) != 'hola':
            return jsonify({'message': 'Contraseña incorrecta'}), 403
            
    response = {'message': 'Hola ' + name} 
    return jsonify(response),203

# Agregar  un nuervo usuario
@app.route('/usuarios', methods=['POST'])
def AgregarUsuario():
    new_usuarios = {
        'id': request.json['id'],
        'email': request.json['email'],
        'birth': request.json['birth'],
        'status': request.json['status'],
        'gender': request.json['gender'],
    }
    usuarios.append(new_usuarios)
    return jsonify({"message": "Usuario agregado  satisfactoriamente","usuarios":usuarios})
    #return jsonify({'usuarios': usuarios})


# Actualizar  un nuevo usuario
@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def ActualizarUsuario(usuario_id):
    usuariosFound = [usuario for usuario in usuarios if usuario['id'] == usuario_id]
    if (len(usuariosFound) > 0):
        usuariosFound[0]['id'] = request.json['id']
        usuariosFound[0]['email'] = request.json['email']
        usuariosFound[0]['birth'] = request.json['birth']
        usuariosFound[0]['status'] = request.json['status']
        usuariosFound[0]['gender'] = request.json['gender']
        return jsonify({
            'message': 'Usuario Actualizado',
            'usuario': usuariosFound[0]
        })
    return jsonify({'message': 'Usuario no encontrado'}),200


# Eliminar  un usuario
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deleteUsuario(usuario_id):
    usuariosFound = [usuario for usuario in usuarios if usuario['id'] == usuario_id]
    if len(usuariosFound) > 0:
        usuarios.remove(usuariosFound[0])
        return jsonify({
            'message': 'Usuario Eliminado',
            'usuarios': usuarios
        })

# Eliminar por email
@app.route('/usuarios/<string:email>', methods=['DELETE'])
def deleteOne(email):
    for i,q in enumerate(usuarios):
      if q['email'] == email:
        del usuarios[i]  
    return jsonify({'quarks' : usuarios}),200


if __name__=='__main__':
    app.run(debug=True,port=4000)
