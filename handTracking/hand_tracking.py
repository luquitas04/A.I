import cv2
import mediapipe as mp

# Inicializa la biblioteca MediaPipe
mp_hands = mp.solutions.hands
# Inicializamos la camara
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.3,
    min_tracking_confidence = 0.3,
) as hands: 
    while cap.isOpened():
        success, image = cap.read() 

        if not success: 
            print("No se puede obtener la imagen de la cámara. Saliendo...")
        
        # Reducir la resolucion de Imagen
        image = cv2.resize(image, (640,480))

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
                
                # Dibujamos las lineas
                connections = mp_hands.HAND_CONNECTIONS
                for connection in connections:
                    start_point_idx = connection[0]
                    end_point_idx = connection[1]

                    if (
                            not results.multi_hand_landmarks[0].landmark[start_point_idx]
                            or not results.multi_hand_landmarks[0].landmark[end_point_idx]
                        ):
                            continue
                    start_coords = (
                                int(
                                    results.multi_hand_landmarks[0].landmark[start_point_idx].x
                                    * image.shape[1]
                                ),
                                int(
                                    results.multi_hand_landmarks[0].landmark[start_point_idx].y
                                    * image.shape[0]
                                ),
                            )
                    end_coords = (
                                int(
                                    results.multi_hand_landmarks[0].landmark[end_point_idx].x
                                    * image.shape[1]
                                ),
                                int(
                                    results.multi_hand_landmarks[0].landmark[end_point_idx].y
                                    * image.shape[0]
                                ),
                            )
                    cv2.line( image, start_coords, end_coords, (0,255,0),2 )

                # extended_fingers = 0
                # finger_tip_points = [
                #     mp_hands.HandLandmark.THUMB_TIP,
                #     mp_hands.HandLandmark.INDEX_FINGER_TIP,
                #     mp_hands.HandLandmark.MIDDLE_FINGER_TIP,                   
                #     mp_hands.HandLandmark.RING_FINGER_TIP,
                #     mp_hands.HandLandmark.PINKY_TIP
                # ]
                # for finger_tip in finger_tip_points:
                #     tip_coords = (
                #         int(results.multi_hand_landmarks[0].landmark[finger_tip].x * image.shape[1]),
                #         int(results.multi_hand_landmarks[0].landmark[finger_tip].y * image.shape[0])  
                #     )
                    
                    
                #     if results.multi_hand_landmarks[0].landmark[finger_tip].y < results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST].y:
                #         extended_fingers +=1
                #         cv2.circle(image, tip_coords,5,(0,0,255),-1)
                    
                # cv2.putText(image, f"Dedos extendidos: {extended_fingers}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

                # Mostrar la imagen con el seguimiento de la mano
                cv2.imshow("Hand Tracking", image)

                if cv2.waitKey(1) & 0xFF == 27: # Presiona la tecla Esc para salir
                    break
        
        # Liberar la cámara y cerrar las ventanas
        # cap.release()
        # cv2.destroyAllWindows()
        # cv2.waitKey(5000)