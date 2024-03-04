from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/runscript', methods=['POST'])
def run_script():
    # Your Python code here
    result = "Script executed"
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
