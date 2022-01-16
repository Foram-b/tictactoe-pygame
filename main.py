import pygame
import math
import mysql.connector


cnx = mysql.connector.connect(user='root', password='abc123foram',
                              host='127.0.0.1',
                              database='projectgame')
cursor = cnx.cursor()

query = ("SELECT login, password FROM user_login")
cursor.execute(query)
login_dict={}





for (login, password) in cursor:
  login_dict[login]=password

def validate_user(login,password):
    if login_dict.get(login) != None and login_dict.get(login) == password:
        return True
    else:

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing SQL query to INSERT a record into the database.
        insert_stmt = (
            "INSERT INTO user_login(login, password)"
            "VALUES (%s, %s)"
        )
        data = (login, password)

        try:
            # Executing the SQL command
            cursor.execute(insert_stmt, data)

            # Commit your changes in the database
            conn.commit()

        except:
            # Rolling back in case of error
            conn.rollback()

        print("Data inserted")

        # Closing the connection
        conn.close()
        return False


def update_score(xlogin,xscore,ylogin,yscore):
    query = ("SELECT xlogin,xscore,ylogin,yscore FROM scoreswins where xlogin={} and ylogin={}".format(xlogin,ylogin))
    cursor.execute(query)
    if len(cursor)>0:
        mycursor = mydb.cursor()

        sql = "UPDATE scoreswins SET scorex = xscore and scorey = yscore WHERE loginx = xlogin and loginy = ylogin"

        mycursor.execute(sql)

        mydb.commit()

        print(mycursor.rowcount, "record(s) affected")
    else:

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Preparing SQL query to INSERT a record into the database.
        insert_stmt = (
            "INSERT INTO scoreswins(loginx, scorex, loginy,scorey)"
            "VALUES (%s, %s, %s, %s)"
        )
        data = (xlogin, xscore, ylogin, yscore)

        try:
            # Executing the SQL command
            cursor.execute(insert_stmt, data)

            # Commit your changes in the database
            conn.commit()

        except:
            # Rolling back in case of error
            conn.rollback()

        print("Data inserted")

        # Closing the connection
        conn.close()








cnx.close()

pygame.init()

# Screen
WIDTH = 600
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))


# Colors
WHITE = (255, 255, 255)
TEAL = (175, 240, 234)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


win.fill(TEAL)
# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (80, 80))

x_won = 0
o_won = 0

# Fonts
END_FONT = pygame.font.SysFont('Ink Free', 50)

# basic font for user typed
base_font = pygame.font.Font(None, 32)

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')

# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color(64,39,17)

color_button = pygame.Color(8,8,8)


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 6:
        print('length should be at least 6')
        val = False

    if len(passwd) > 20:
        print('length should be not be greater than 8')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isalpha() for char in passwd):
        print('Password should have at least one Alphabet')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#%')
        val = False
    if val:
        return val



class Button:
    def __init__(self, screen, text, X, Y):
        self.input_rect = pygame.Rect(X, Y, 140, 32)
        self.color = color_button
        self.text = text
        self.text_surface = base_font.render(self.text, True, (255,255,255))
        self.screen = screen
        pygame.draw.rect(self.screen, self.color, self.input_rect)
        # render at position stated in arguments
        self.screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self.input_rect.w = max(140, self.text_surface.get_width() + 10)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                return True
        return False


class Textbox:
    def __init__(self, screen, X, Y, text) -> object:
        self.input_rect = pygame.Rect(X, Y, 140, 32)
        self.color = color_passive
        self.user_text = ""
        self.text = text
        self.active = False
        self.text_surface = base_font.render(self.user_text, True, (8,8,8))
        self.screen = screen
        pygame.draw.rect(self.screen, self.color, self.input_rect)
        self.label_surface = base_font.render(self.text, True, (8,8,8))
        self.screen.blit(self.label_surface, (self.input_rect.x - 180, self.input_rect.y + 5))
        self.change_mode()

    def update_for_event(self, event):
        """
        This function should be called for each event that is happening with Event as parameter.
        :param event: Event which is happened.
        :type event:
        :return:
        :rtype:None
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                if not self.active:
                    self.active = True
                    self.change_mode()
            else:
                if self.active:
                    self.active = False
                    self.change_mode()

        if self.active:
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    self.user_text = self.user_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    self.user_text += event.unicode
                self.update_text()

    def change_mode(self):
        if self.active:
            self.color=color_active
        else:
            self.color=color_passive
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(self.screen, self.color, self.input_rect)
        self.update_text()

    def update_text(self):
        self.text_surface = base_font.render(self.user_text, True, (255,255,255))
        # render at position stated in arguments
        self.screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self.input_rect.w = max(140, self.text_surface.get_width() + 10)

def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)

def start_game(xlogin, ologin, xpass, opass):
    """
    this will validate login screen and start the game.
    :param xlogin:
    :type xlogin:
    :param ologin:
    :type ologin:
    :param xpass:
    :type xpass:
    :param opass:
    :type opass:
    :return:
    :rtype:
    """
    return True


def show_login():

    clock = pygame.time.Clock()

    xlogin = Textbox(win, 200, 100, "X LOGIN")
    xpassword = Textbox(win, 200, 140, "X PASSWORD")

    ologin = Textbox(win, 200, 300, "O LOGIN")
    opassword = Textbox(win, 200, 340, "O PASSWORD")

    start_button = Button(win, "Start >", 450, 500)

    # display.flip() will update only a portion of the
    # screen to updated, not full area
    pygame.display.flip()

    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)

    while True:
        for event in pygame.event.get():
            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.MOUSEBUTTONDOWN == event.type or pygame.KEYDOWN == event.type:
                xlogin.update_for_event(event)
                ologin.update_for_event(event)
                xpassword.update_for_event(event)
                opassword.update_for_event(event)
                # display.flip() will update only a portion of the
                # screen to updated, not full area
                pygame.display.flip()

            if pygame.MOUSEBUTTONDOWN == event.type:
                start = start_button.clicked(event)
                pygame.display.flip()
                if start:
                    if password_check(xpassword.user_text) and \
                        password_check(opassword.user_text) and \
                            xlogin.user_text.strip() != "" and \
                            ologin.user_text.strip() != "" and \
                            xlogin.user_text != ologin.user_text:
                        print("Lets Begin !")
                        return xlogin.user_text, ologin.user_text, xpassword.user_text, opassword.user_text
                    else:
                        print("Correct Errors for starting game.")







def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array):
    global x_turn, o_turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)

                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)


# Checking if someone has won
def has_won(game_array, x_login, o_login):
    global x_won, o_won
    # Checking rows

    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            if game_array[row][0][2].upper() == 'X':
                x_won = x_won + 1
                who = x_login
            else:
                o_won = o_won + 1
                who = o_login
            display_message(game_array[row][0][2].upper() + ": " + who + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            if game_array[row][0][2].upper() == 'X':
                x_won = x_won + 1
                who = x_login
            else:
                o_won = o_won + 1
                who = o_login
            display_message(game_array[0][col][2].upper() + ": " + who + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        if game_array[row][0][2].upper() == 'X':
            x_won = x_won + 1
            who = x_login
        else:
            o_won = o_won + 1
            who = o_login
        display_message(game_array[0][0][2].upper() + ": " + who + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        if game_array[row][0][2].upper() == 'X':
            x_won = x_won + 1
            who = x_login
        else:
            o_won = o_won + 1
            who = o_login
        display_message(game_array[0][2][2].upper() + ": " + who + " has won!")
        return True

    return False


def has_drawn(game_array):
    # TODO:logic can be improved to draw earlier
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def main(x_login, o_login):
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False


    pygame.display.update()

    game_array = initialize_grid()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)

        render()

        if has_won(game_array, x_login, o_login) or has_drawn(game_array):
            run = False


if __name__ == '__main__':
    x_login, o_login, x_pass, o_pass = show_login()
    login_status=validate_user(x_login, x_pass) and validate_user(o_login, o_pass)
    if not login_status:
        print("enter correct login details and retry")
    while login_status:
        #get results
        pygame.display.set_caption("TicTacToe  X:{}-{}  O:{}-{}".format(x_login, x_won, o_login, o_won))
        main(x_login, o_login)
