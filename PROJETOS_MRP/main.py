import plano_mestre

while True:    
    escolha = plano_mestre.menu_principal([1,2,3,4,5,6])
    if escolha == "6":
        plano_mestre.separação()
        print("ENCERRANDO PROGRAMA!".center(50))
        plano_mestre.separação()
        break
