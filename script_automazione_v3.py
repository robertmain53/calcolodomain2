# Dentro il ciclo principale
pagina_template = classifica_pagina(file_path) # Funzione che usa il report

if pagina_template == "Template A":
    # Logica di ristrutturazione a 2 colonne (quella che avevamo)
    logica_per_template_A(soup)
elif pagina_template == "Template B":
    # Logica per "Doppio Body": molto più complessa.
    # Deve estrarre il contenuto dal *secondo* body e ricostruire
    # l'intera pagina da zero.
    logica_per_template_B(soup)
elif pagina_template == "Template C":
    # Logica per "Orfane Pulite": sicura.
    # Possiamo applicare il layout a 2 colonne e aggiungere header/footer.
    logica_per_template_C(soup)
else:
    # Logica di sicurezza: non fare nulla, segnala solo
    log_errore(file_path)