import pygame
import random

pygame.init()



#Configurações:
largura, altura = 800, 600
chao = altura - 50
velocidade = 5
gravidade = 0.7
fonte = pygame.font.Font("Imagens\Fonte\SuperMario256.ttf", 50)


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

na_plataforma = False  #Para identificar se o player está tocando o chão


plataformas_group = pygame.sprite.Group()
for plataforma in plataformas:
    plataformas_group.add(plataforma)
    



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

player = Jogador()
player_group = pygame.sprite.Group()
player_group.add(player)


#Funções:



def desenhar():
    #Limpar tela a cada quadro, evitando sobreposição
    tela.fill(preto)
    
    plataformas_group.draw(tela)

    moeda_group.draw(tela)

    player_group.draw(tela)

    label_moedas = fonte.render(f"Moedas: {contador_moeda}", True, branco)
    tela.blit(label_moedas, (20,20))

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
    
    if teclas[pygame.K_w] and na_plataforma:  # pulo nas plataformas
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
    global na_plataforma
    na_plataforma = False
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
                na_plataforma = True

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
        
rodando = True


#Loop principal
while rodando == True:
    pygame.time.delay(30)
    
    eventos()

    inputs()
    
    fisica()

    colisoes()
    
    desenhar() 
    
pygame.QUIT