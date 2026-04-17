import face_recognition

def match_faces(known, unknown):
    known_img = face_recognition.load_image_file(known)
    unknown_img = face_recognition.load_image_file(unknown)

    k_enc = face_recognition.face_encodings(known_img)
    u_enc = face_recognition.face_encodings(unknown_img)

    if not k_enc or not u_enc:
        return False

    return face_recognition.compare_faces([k_enc[0]], u_enc[0])[0]





    