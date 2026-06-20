import pygame
import random

pygame.init()



#Configurações:
largura, altura = 800, 600
chao = altura - 50
velocidade = 5
gravidade = 0.7
fonte = pygame.font.Font("Imagens\Fonte\SuperMario256.ttf", 50)
estado_do_jogo = "partida"
#Partida, Fim e Inicio

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Testando")


#Cores:
vermelho = (255, 0, 0)
preto = (0, 0, 0)
verde = (0, 255, 0)
dourado = (255, 215, 0)
branco = (255, 255, 255)


#Objetos:
vel_x = 0
vel_y = 0

#Plataformas

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem = pygame.image.load("Imagens\Plataforma\plataforma.png")
        self.image = pygame.transform.scale(imagem, (200, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


plataformas =[
    Plataforma(400, 400),
    Plataforma(100, 200),
    Plataforma(600, 150)
]




plataformas_group = pygame.sprite.Group()
for plataforma in plataformas:
    plataformas_group.add(plataforma)
    
#Espinhos
class Espinhos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        imagem = pygame.image.load('Imagens\Espinhos\espinhos.png')
        self.image = pygame.transform.scale(imagem, (100, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
base_espinhos = altura-20
espinhos = [
    Espinhos(100, base_espinhos),
    Espinhos(400, base_espinhos),
    Espinhos(700, base_espinhos)
]
espinhos_group = pygame.sprite.Group()
for espinho in espinhos:
    espinhos_group.add(espinho)
#Moeda
class Moeda(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imagem = pygame.image.load("Imagens\Moeda\SMB_Sprite_Coin.png")
        self.image = pygame.transform.scale(imagem, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 300

moeda = Moeda()
moeda_group = pygame.sprite.Group()
moeda_group.add(moeda)

contador_moeda = 0


# Personagem
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  
        imagem = pygame.image.load("Imagens\Personagem\sprite_player.png")
        self.image = pygame.transform.scale(imagem, (64, 85))
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 250
        self.vida = 3
        self.tomou_dano = False
        self.morto = False
        self.baleia = False
        self.na_plataforma = False  #Para identificar se o player está tocando o chão
    def perder_vida(self):
        global estado_do_jogo
        if self.vida > 0 and self.tomou_dano == False:
            self.vida -=1
        if self.vida == 0:
            self.morto = True
            estado_do_jogo = "fim"

player = Jogador()
player_group = pygame.sprite.Group()
player_group.add(player)

#Poder - Baleia
class Baleia(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  
        imagem = pygame.image.load("Imagens\Poderes\Baleia.png")
        self.image = pygame.transform.scale(imagem, (140, 140))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

baleia = Baleia()
baleia_group = pygame.sprite.Group()
baleia_group.add(baleia)

class Biscoito(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  
        imagem = pygame.image.load("Imagens\Poderes\Cookie.png")
        self.image = pygame.transform.scale(imagem, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 100

cookie = Biscoito()
cookie_group = pygame.sprite.Group()
cookie_group.add(cookie)




#Funções:


def desenhar():
    #Limpar tela a cada quadro, evitando sobreposição
    tela.fill(preto)
    
    plataformas_group.draw(tela)

    moeda_group.draw(tela)

    player_group.draw(tela)

    espinhos_group.draw(tela)

    cookie_group.draw(tela)

    label_moedas = fonte.render(f"Moedas: {contador_moeda}", True, branco)
    tela.blit(label_moedas, (20,20))

    label_vida = fonte.render(f"Vida(s): {player.vida}", True, branco)
    tela.blit(label_vida, (largura-300, 20))

    #Atualizar a tela
    pygame.display.flip()

def eventos():    #Fecha o game
    global rodando
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            rodando = False

def inputs():
    global vel_x
    global vel_y
    #Movimentação, identifica as teclas pressionadas e aumenta a posição
    teclas = pygame.key.get_pressed()

    vel_x = 0

    if teclas[pygame.K_a]:   #andar para a esquerda
        vel_x = -velocidade

    if teclas[pygame.K_d]:   #andar para a direita
        vel_x = velocidade

    if teclas[pygame.K_w] and player.rect.y >= chao - 50:  # pulo, somente no chão
        vel_y = -velocidade*4
    
    if teclas[pygame.K_w] and player.na_plataforma:  # pulo nas plataformas
        vel_y = -velocidade*4

def fisica():                                                                                                                                                   
    global vel_y
    # aplica gravidade
    vel_y += gravidade

    #Movimentação do player
    player.rect.x += vel_x
    player.rect.y += vel_y

    # Limites da tela
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > largura:
        player.rect.right = largura

def colisoes():
    global vel_y
    
    player.na_plataforma = False
    global contador_moeda  

    # colisão com chão
    if player.rect.y >= chao - 50:
        player.rect.y = chao - 50
        vel_y = 0
        
    
    # Colisão com a plataforma:
    for plat in plataformas:
        #Impedir que a moeda pare em cima de alguma plataforma
        if moeda.rect.colliderect(plat):
            moeda.rect.x = random.randint(0, largura - moeda.rect.width)
            moeda.rect.y = random.randint(0, altura - moeda.rect.height)
        if player.rect.colliderect(plat):

        # Colisão vindo de cima (caindo)
            if vel_y >= 0 and player.rect.bottom - vel_y <= plat.rect.top +1:
                player.rect.bottom = plat.rect.top
                vel_y = 0
                player.na_plataforma = True

        # Colisão vindo de baixo (batendo a cabeça)
            elif vel_y < 0 and player.rect.top - vel_y >= plat.rect.bottom -1:
                player.rect.top = plat.rect.bottom
                vel_y = 0
        
        # Colisão vindo da lateral:
            elif vel_x > 0 and player.rect.right - vel_x <= plat.rect.left + 1:
                player.rect.right = plat.rect.left
            elif vel_x < 0 and player.rect.left + vel_x <= plat.rect.right - 1:
                player.rect.left = plat.rect.right
        
    # Colisão com a Moeda:
    if player.rect.colliderect(moeda):
        #Randomiza a posição da moeda sempre que o player a toca
        moeda.rect.x = random.randint(0, largura - moeda.rect.width)
        moeda.rect.y = random.randint(0, altura - moeda.rect.height)
        contador_moeda += 1
    
    #Colisão com os espinhos:

    espinhos_colididos = pygame.sprite.spritecollide(player, espinhos_group, False)
    if espinhos_colididos:
        player.perder_vida()
        player.tomou_dano = True
    else:
        player.tomou_dano = False

    #Pegar cookie:
    cookies_pegos = pygame.sprite.spritecollide(player, cookie_group, True)
    if cookies_pegos:
        player.baleia = True



def final():
    tela.fill(preto)
    label_pontuacao = fonte.render(f"Seus pontos: {contador_moeda}", True, dourado)
    tela.blit(label_pontuacao, (largura/2-200, altura/2-200))
    label_fim = fonte.render("Fim de Jogo", False, vermelho)
    tela.blit(label_fim, (largura/2-200, altura/2-70))
    pygame.display.flip()
        

def poder_baleia():

    global vel_y

    if player.baleia == True:
        teclas = pygame.key.get_pressed()
        if vel_y != 0 and teclas[pygame.K_s]:
            vel_y += 10
            baleia.rect.center = player.rect.center
            baleia_group.draw(tela)
            #Colisão baleia e espinhos:
            espinhos_esmagados = pygame.sprite.spritecollide(baleia, espinhos_group, True)
            player.tomou_dano = True
            if espinhos_esmagados:
                player.vida += 1

            pygame.display.flip()



rodando = True


#Loop principal
while rodando == True:
    pygame.time.delay(30)

    eventos()

    inputs()
    
    if estado_do_jogo == "partida":
        
        fisica()

        colisoes()

        
        
        desenhar() 

        poder_baleia()
    
    if estado_do_jogo == "fim":
        final()

    
pygame.QUIT