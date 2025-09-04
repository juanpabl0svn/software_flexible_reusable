# 🚨 Code Smells Identificados

## 1. God Class
- Todo estaba dentro de una sola clase gigante (**Game**).
- La clase manejaba **jugadores, preguntas, lógica de penalización, movimientos**, etc.
- Esto la hacía difícil de mantener y extender.

---

## 2. Métodos Largos
- Ejemplo: el método `roll` tenía **muchas responsabilidades**:
  - Tirar dado 🎲  
  - Mover jugador 🏃  
  - Verificar penalización 🚫  
  - Seleccionar categoría ❓  
  - Hacer preguntas 📝  

---

## 3. Complejidad Cognitiva
- Existían **muchos `if`, ciclos y condiciones anidadas**.  
- Esto dificultaba entender la lógica y aumentaba el riesgo de errores.

---

## 4. Código Duplicado
- Se repetía lógica en:
  - La **selección de categorías**.  
  - El **manejo de jugadores**.

---

## 5. Grupo de Datos
- Datos como:
  - `name`  
  - `purse`  
  - `place`  
  - `in_penalty_box`  

Estaban juntos sin encapsularse en un objeto.  
➡️ Se resolvió creando la clase **`Player`**.




### Integrantes

````bash
Juan Pablo Aguirre
Luigi Nieves
Juan Pablo Sanchez