import cv2
import mediapipe as mp

# Inicializa la biblioteca MediaPipe
mp_hands = mp.solutions.hands
# Inicializamos la camara
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5,
) as hands: 
    while cap.isOpened():
        success, image = cap.read() 

        if not success: 
            print("No se puede obtener la imagen de la cámara. Saliendo...")
            
        # Convertir la imagen de BGR a RGB 
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Realiza la deteccion de manos
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks: 
            for hand_landmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalized_landmark = hand_landmarks.landmark[point]
                    pixel_coords = (
                        int(normalized_landmark.x * image.shape[1]),
                        int(normalized_landmark.y * image.shape[0]),
                    )

                    # Dibujar circulos en los puntos de referencia 
                    cv2.circle(image, pixel_coords, 5, (0,255,0), -1)
                
                hand_landmarks_list = [
                    mp_hands.HandLandmark.WRIST,
                    mp_hands.HandLandmark.THUMB_CMC,
                    mp_hands.HandLandmark.THUMB_MCP,
                    mp_hands.HandLandmark.THUMB_IP,
                    mp_hands.HandLandmark.THUMB_TIP,
                    mp_hands.HandLandmark.INDEX_FINGER_MCP,
                    mp_hands.HandLandmark.INDEX_FINGER_PIP,
                    mp_hands.HandLandmark.INDEX_FINGER_TIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                    mp_hands.HandLandmark.RING_FINGER_MCP,
                    mp_hands.HandLandmark.RING_FINGER_PIP,
                    mp_hands.HandLandmark.RING_FINGER_TIP,
                    mp_hands.HandLandmark.PINKY_MCP,
                    mp_hands.HandLandmark.PINKY_PIP,
                    mp_hands.HandLandmark.PINKY_TIP,
                ]                                   
                for i in range(0, len(hand_landmarks_list) -1 , 4):
                    for j in range(i,i + 4):
                        if (
                            not results.multi_hand_landmarks[0].landmark[hand_landmarks_list[j]]
                            or not results.multi_hand_landmarks[0].landmark[hand_landmarks_list[j + 1]]
                        ):
                            break
                        start_point = (
                                int(
                                    results.multi_hand_landmarks[0].landmark[hand_landmarks_list[j]].x
                                    * image.shape[1]
                                ),
                                int(
                                    results.multi_hand_landmarks[0].landmark[hand_landmarks_list[j]].y
                                    * image.shape[0]
                                ),
                            )
                        end_point = (
                                int(
                                    results.multi_hand_landmarks[0].landmark[hand_landmarks_list[j + 1]].x
                                    * image.shape[1]
                                ),
                                int(
                                    results.multi_hand_landmarks[0].landmark[hand_landmarks_list[j + 1]].y
                                    * image.shape[0]
                                ),
                            )
                        cv2.line( image, start_point, end_point, (0,255,0),2 )
                # Mostrar la imagen con el seguimiento de la mano
                cv2.imshow("Hand Tracking", image)

                if cv2.waitKey(1) & 0xFF == 27: # Presiona la tecla Esc para salir
                    break
        
        # Liberar la cámara y cerrar las ventanas
        cap.release()
        cv2.destroyAllWindows()
        # cv2.waitKey(5000)