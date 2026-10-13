
import pygame
import os
import random

# ==========================
# CONFIGURAÇÕES DO JOGO
# ==========================

screenWidth = 500
screenHeight = 800

# Inicializa o Pygame
pygame.init()

# ==========================
# CARREGAMENTO DAS IMAGENS
# ==========================

# Carrega as imagens e aumenta suas dimensões
backgroundImage = pygame.transform.scale2x(
    pygame.image.load(os.path.join('img', 'bg.png'))
)

pipeImage = pygame.transform.scale2x(
    pygame.image.load(os.path.join('img', 'pipe.png'))
)

# Lista com as imagens usadas na animação do pássaro
birdImage = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('img', 'bird1.png'))
    ),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('img', 'bird2.png'))
    ),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join('img', 'bird3.png'))
    )
]

floorImage = pygame.transform.scale2x(
    pygame.image.load(os.path.join('img', 'base.png'))
)

# ==========================
# CONFIGURAÇÃO DA PONTUAÇÃO
# ==========================

pygame.font.init()
fontPoint = pygame.font.SysFont('arial', 50)


# ==========================
# CLASSE DO PÁSSARO
# ==========================

class Bird:
    # Atributos compartilhados pelos pássaros
    img = birdImage
    maxRotation = 25
    rotationVelocity = 20
    animationTime = 5

    def __init__(self, x, y):
        # Posição inicial do pássaro
        self.x = x
        self.y = y

        # Atributos do movimento
        self.angulo = 0
        self.velocity = 0
        self.height = self.y
        self.time = 0

        # Atributos da animação
        self.imageContagem = 0
        self.image = self.img[0]

    def jump(self):
        """Aplica a velocidade inicial do salto."""
        self.velocity = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        """Calcula a posição vertical e a rotação do pássaro."""

        # Calcula o deslocamento usando o tempo e a velocidade
        self.time += 1
        deslocamento = (
            1.5 * (self.time ** 2)
            + self.velocity * self.time
        )

        # Limita a velocidade de queda
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        # Atualiza a posição vertical
        self.y += deslocamento

        # Ajusta o ângulo conforme o pássaro sobe ou cai
        if deslocamento < 0 or self.y < (self.height + 50):
            if self.angulo < self.maxRotation:
                self.angulo = self.maxRotation
        else:
            if self.angulo > -90:
                self.angulo -= self.rotationVelocity

    def desenhar(self, screen):
        """Atualiza a animação e desenha o pássaro na tela."""

        self.imageContagem += 1

        # Alterna as imagens para simular o movimento das asas
        if self.imageContagem < self.animationTime:
            self.image = self.img[0]

        elif self.imageContagem < self.animationTime * 2:
            self.image = self.img[1]

        elif self.imageContagem < self.animationTime * 3:
            self.image = self.img[2]

        elif self.imageContagem < self.animationTime * 4:
            self.image = self.img[1]

        else:
            self.image = self.img[0]
            self.imageContagem = 0

        # Quando está caindo muito, mantém uma imagem específica
        if self.angulo <= -80:
            self.image = self.img[1]
            self.imageContagem = self.animationTime * 2

        # Rotaciona a imagem de acordo com o ângulo atual
        imagemRotacionada = pygame.transform.rotate(
            self.image, self.angulo
        )

        # Mantém o centro da imagem na mesma posição após a rotação
        posCentro = self.image.get_rect(
            topleft=(self.x, self.y)
        ).center

        retangulo = imagemRotacionada.get_rect(center=posCentro)

        # Desenha o pássaro
        screen.blit(imagemRotacionada, retangulo.topleft)

    def get_mask(self):
        """Cria uma máscara para detectar colisões precisas."""
        return pygame.mask.from_surface(self.image)


# ==========================
# CLASSE DOS CANOS
# ==========================

class Pipe:
    distance = 200
    velocity = 5

    def __init__(self, x):
        # Posição horizontal do cano
        self.x = x

        # Posições verticais
        self.height = 0
        self.posTopo = 0
        self.pos_base = 0

        # Imagem do cano superior e inferior
        self.upPipe = pygame.transform.flip(
            pipeImage, False, True
        )
        self.downPipe = pipeImage

        # Controla se o pássaro já passou pelo cano
        self.passou = False

        # Define a altura inicial dos canos
        self.defHeight()

    def defHeight(self):
        """Gera uma altura aleatória para o conjunto de canos."""

        self.height = random.randrange(50, 450)

        self.pos_base = (
            self.height - self.upPipe.get_height()
        )

        self.posTopo = self.height + self.distance

    def move(self):
        """Move os canos para a esquerda."""
        self.x -= self.velocity

    def paint(self, screen):
        """Desenha os canos superior e inferior."""

        screen.blit(
            self.upPipe,
            (self.x, self.posTopo)
        )

        screen.blit(
            self.downPipe,
            (self.x, self.pos_base)
        )

    def crash(self, bird):
        """Verifica se o pássaro colidiu com algum cano."""

        birdMask = bird.get_mask()

        upMask = pygame.mask.from_surface(self.upPipe)
        baseMask = pygame.mask.from_surface(self.downPipe)

        # Calcula a distância entre o pássaro e cada cano
        upDistance = (
            self.x - bird.x,
            self.posTopo - round(bird.y)
        )

        baseDistance = (
            self.x - bird.x,
            self.pos_base - round(bird.y)
        )

        # Verifica a sobreposição entre as máscaras
        upPoint = birdMask.overlap(upMask, upDistance)
        basePoint = birdMask.overlap(baseMask, baseDistance)

        # Se houver sobreposição, ocorreu uma colisão
        return bool(upPoint or basePoint)


# ==========================
# CLASSE DO CHÃO
# ==========================

class Floor:
    velocity = 5
    width = floorImage.get_width()
    image = floorImage

    def __init__(self, y):
        # Posição vertical do chão
        self.y = y

        # Duas imagens permitem criar um chão contínuo
        self.x0 = 0
        self.x1 = self.width

    def move(self):
        """Move o chão e reposiciona as imagens para criar repetição."""

        self.x0 -= self.velocity
        self.x1 -= self.velocity

        # Reposiciona a primeira imagem quando sai da tela
        if self.x0 + self.width < 0:
            self.x0 = self.x1 + self.width

        # Reposiciona a segunda imagem quando sai da tela
        if self.x1 + self.width < 0:
            self.x1 = self.x0 + self.width

    def paint(self, screen):
        """Desenha as duas imagens do chão."""

        screen.blit(self.image, (self.x0, self.y))
        screen.blit(self.image, (self.x1, self.y))


# ==========================
# DESENHO DA TELA
# ==========================

def paintScreen(screen, birds, pipes, ground, score):
    """Desenha todos os elementos do jogo."""

    # Desenha o fundo
    screen.blit(backgroundImage, (0, 0))

    # Desenha os pássaros
    for current_bird in birds:
        current_bird.desenhar(screen)

    # Desenha os canos
    for current_pipe in pipes:
        current_pipe.paint(screen)

    # Renderiza a pontuação
    text = fontPoint.render(
        f"Pontuação: {score}", True, (255, 255, 255)
    )

    screen.blit(
        text,
        (screenWidth - 10 - text.get_width(), 10)
    )

    # Desenha o chão por cima dos outros elementos
    ground.paint(screen)

    # Atualiza a imagem exibida
    pygame.display.update()


# ==========================
# FUNÇÃO PRINCIPAL
# ==========================

def main():

    # Cria os objetos iniciais do jogo
    birds = [Bird(230, 350)]
    ground = Floor(730)
    pipes = [Pipe(700)]

    # Configura a janela
    screen = pygame.display.set_mode(
        (screenWidth, screenHeight)
    )

    pygame.display.set_caption("Flappy Bird")

    # Pontuação e controle de FPS
    score = 0
    clock = pygame.time.Clock()

    rodando = True

    while rodando:

        # Mantém o jogo em 30 quadros por segundo
        clock.tick(30)

        # ==========================
        # EVENTOS DO JOGADOR
        # ==========================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            elif event.type == pygame.KEYDOWN:

                # Pressionar espaço faz o pássaro pular
                if event.key == pygame.K_SPACE:
                    for current_bird in birds:
                        current_bird.jump()

        # Encerra o jogo se a janela for fechada
        if not rodando:
            break

        # ==========================
        # MOVIMENTAÇÃO
        # ==========================

        for current_bird in birds:
            current_bird.move()

        ground.move()

        # ==========================
        # MOVIMENTAÇÃO E COLISÕES
        # ==========================

        addPipe = False
        removePipes = []

        for current_pipe in pipes:

            # Percorre uma cópia para permitir remover pássaros
            # sem alterar a lista durante a iteração
            for current_bird in birds[:]:

                # Verifica colisão com os canos
                if current_pipe.crash(current_bird):
                    birds.remove(current_bird)
                    continue

                # Verifica se o pássaro passou pelo cano
                if (
                    not current_pipe.passou
                    and current_bird.x > current_pipe.x
                ):
                    current_pipe.passou = True
                    addPipe = True

            # Move o cano
            current_pipe.move()

            # Marca canos que saíram completamente da tela
            if (
                current_pipe.x + current_pipe.upPipe.get_width() < 0
            ):
                removePipes.append(current_pipe)

        # ==========================
        # PONTUAÇÃO E NOVOS CANOS
        # ==========================

        if addPipe:
            score += 1
            pipes.append(Pipe(600))

        # Remove os canos que saíram da tela
        for current_pipe in removePipes:
            pipes.remove(current_pipe)

        # ==========================
        # LIMITES DA TELA
        # ==========================

        # Também usamos uma cópia para remover com segurança
        for current_bird in birds[:]:

            if (
                current_bird.y + current_bird.image.get_height() >= 730
                or current_bird.y < 0
            ):
                birds.remove(current_bird)

        # ==========================
        # ATUALIZAÇÃO DA TELA
        # ==========================

        paintScreen(
            screen, birds, pipes, ground, score
        )

    # Encerra o Pygame ao sair do loop
    pygame.quit()


# Executa o jogo somente quando este arquivo é iniciado diretamente
if __name__ == "__main__":
    main()
