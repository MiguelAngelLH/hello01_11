from Flask import Flask, render_template

app = Flask(__name__)

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    """Página para buscar algo."""
    return render_template('buscar.html')

@app.route("/prueba", methods=["GET", "POST"])
def prueba():
    """Página para probar el DOM."""
    return render_template('buscar.html')

if __name__ == '__main__':
    app.run(debug=True)
