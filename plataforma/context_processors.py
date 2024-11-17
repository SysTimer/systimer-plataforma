from .models import Empresa



def empresa(request):
    codigo_empresa = request.session.get('emp_cod')
    
    if codigo_empresa:
        empresa = Empresa.objects.filter(EMP_COD=codigo_empresa).first()
        
        if empresa:
            print('Empresa: ', empresa.EMP_NOME)
            return {'empresa': empresa}
        else:
            print('Empresa não encontrada para o código:', codigo_empresa)
            return {'empresa': None}  
    else:
        print('Código de empresa não encontrado na sessão.')
        return {'empresa': None}  
