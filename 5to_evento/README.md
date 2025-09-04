CODE SMELL

God Class: todo estaba dentro de una sola clase gigante (Game), manejando jugadores, preguntas, lógica de penalización, movimientos, etc.

Métodos largos: había métodos como roll con muchas responsabilidades (tirar dado, mover jugador, verificar penalización, preguntar, etc.).

Complejidad cognitiva: muchos if, ciclos, y condiciones anidadas.

Código duplicado: repetición en la selección de categorías y en el manejo de jugadores.

Grupo de datos: datos como name, purse, place, in_penalty_box estaban juntos sin encapsularlos en un objeto (Player).