def calc_tiempo_macollaje( mes_siembra ):
    tiempos_macollaje = {
        "enero": 2.5,
        "febrero": 2.8,
        "marzo": 2.2,
        "abril": 1.9,
        "mayo": 2.1,
    }
    mes_siembra_lower = mes_siembra.lower()
    if mes_siembra_lower in tiempos_macollaje:
        tiempo_macollaje = tiempos_macollaje[mes_siembra_lower]
        return f"el tiempo de macollaje si se siembra en '{mes_siembra}', es de en aproximadamente {tiempo_macollaje} meses"
    else: 
        return "No se encontro el mes de siembra"
    
mes_siembra = input("Mes de siembra: ")
resultado = calc_tiempo_macollaje(mes_siembra)
print(resultado)