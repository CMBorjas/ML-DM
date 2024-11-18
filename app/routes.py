from flask import request, redirect

@app.route('/upload', methods=['POST'])
def upload_map():
    map_file = request.files['map']
    map_file.save(f"app/maps/{map_file.filename}")
    return redirect('/')
