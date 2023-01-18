- Versione aggiornata della demo, con self collision check e verifica dell'uomo nello spazio operativo nel flag_stop_server. 

- Le coordinate dello scheletro sono riferite nel sistema di riferimento del robot.

- Il robot compie n cicli di lavoro prima di fermarsi. 

- Raggio delle capsule ridotto modificando contributo Sr.

- Aggiunta dei file launch per lanciare contemporaneamente i tre servizi, il move group e franka control.

- Creazione di cartella con nome del tester.

- Lo streaming della telecamera viene salvato come video in formato .avi nella cartella.

- Aggiunto calc_stop_duration_static_server.

- Diversificato flag_stop_service a seconda che venga lanciato nel file launch di static, for o ott.

- Diversificato stop_trajectory per esperimenti con file launch di static, for o ott.

- Salvataggio dati su cartella con relativi tempi.

- Aggiunto calibrator.launch per calibrazione autonoma.

- Migliorato il calcolo delle capsule in flag_stop_ott_server.py

- Modificato calcolo capsule.

- Modificata ripartenza.

- Spostata funzione di callback di q e q_p in Execute task e aggiunto sleep per partire nell'istante zero con registrazione dati

- Aggiunto check per lunghezza segmenti uomo.

- Tolti keypoints superflui da util.py.

- Modificato ciclo while per aspettare fine di traiettoria di stop.

- Aggiunto programma tau_calculator.py per calcolare le coppie in post processing.
