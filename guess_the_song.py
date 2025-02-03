import os
import pygame
import time
import pyttsx3
import random

pygame.init()

screen_width = 1200
screen_height = 600

white = (255, 255, 255)
black = (0, 0, 0)
violet = (138, 43, 226)

font_title = pygame.font.Font(None, 72)
font_instruction = pygame.font.Font(None, 36)
font_info = pygame.font.Font(None, 28)
font_score = pygame.font.Font(None, 48)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_song(song_file, duration):
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()
    time.sleep(duration)
    pygame.mixer.music.stop()

def get_choices():
    music_directory = "music"
    songs = os.listdir(music_directory)
    random.shuffle(songs)
    return [song.replace(".mp3", "") for song in songs]

def draw_background(image_path):
    screen.fill(black)
    img = pygame.image.load(image_path)
    img = pygame.transform.scale(img, (screen_width, screen_height))
    img_rect = img.get_rect()
    img_rect.topleft = (0, 0)
    screen.blit(img, img_rect)

    pygame.display.flip()

def draw_blank_background():
    screen.fill(black)
    pygame.display.flip()

def draw_title(background_image):
    draw_background(background_image)

    title_text = font_title.render("Guess the Song Game", True, violet)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(title_text, title_rect)
    pygame.display.flip()

def draw_play_button(background_image):
    draw_background(background_image)

    play_button_text = font_instruction.render("Play", True, white)
    play_button_rect = play_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    pygame.draw.rect(screen, violet, (play_button_rect.x - 10, play_button_rect.y - 10, play_button_rect.width + 20, play_button_rect.height + 20))
    screen.blit(play_button_text, play_button_rect)

    pygame.display.flip()

    play_button_clicked = False
    while not play_button_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button_rect.collidepoint(x, y):
                    play_button_clicked = True

def draw_choices_with_lives(choices, selected_choice, level, round_num, score, rounds_remaining, lives, background_image, choice_timer, choice_timer_duration):
    draw_background(background_image)

    # Display level, round, score, and rounds remaining on the right side of the screen
    info_text = font_info.render(f"Level: {level} | Round: {round_num} | Score: {score} | Rounds Remaining: {rounds_remaining}",
                                 True, violet)
    info_text_rect = info_text.get_rect()
    info_text_rect.x = screen_width - info_text_rect.width - 10
    info_text_rect.y = 10
    screen.blit(info_text, info_text_rect)

    # Display lives on the left side of the screen
    lives_text = font_info.render(f"Lives: {lives}", True, violet)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.x = 10
    lives_text_rect.y = 10
    screen.blit(lives_text, lives_text_rect)

    # Center the instruction_text at the top of the choices
    instruction_text = font_instruction.render("Choose the correct answer:", True, violet)
    instruction_text_rect = instruction_text.get_rect(center=(screen_width // 2, 170))
    screen.blit(instruction_text, instruction_text_rect)

    # Calculate the total height of the instruction text and choices
    total_height = len(choices) * 50 + instruction_text.get_height()

    # Display choices centered on the screen
    for i, choice in enumerate(choices):
        text = font_instruction.render(f"{chr(65 + i)}. {choice}", True, violet)
        text_rect = text.get_rect(center=(screen_width // 2, (screen_height - total_height) // 2 + instruction_text.get_height() + i * 50))
        screen.blit(text, text_rect)

    # Draw the timer
    time_left = max(0, choice_timer + choice_timer_duration - pygame.time.get_ticks())
    timer_text_color = (138, 43, 226)

    # Change color to red when less than 3 seconds left
    if time_left < 3000:
        timer_text_color = (255, 0, 0)

    timer_text = font_info.render(f"Time left: {time_left // 1000} seconds", True, timer_text_color)
    timer_rect = timer_text.get_rect(center=(screen_width // 2, screen_height - 50))
    screen.blit(timer_text, timer_rect)

    # Draw a visual representation of the timer
    timer_bar_length = (time_left / choice_timer_duration) * (screen_width - 20)
    timer_bar_rect = pygame.Rect(10, screen_height - 30, timer_bar_length, 20)
    pygame.draw.rect(screen, (0, 255, 0), timer_bar_rect)

    pygame.display.update()

def draw_final_score(score, background_image):
    draw_background(background_image)

    final_score_text = font_score.render(f"Score: {score}", True, violet)
    screen.blit(final_score_text,
                (screen_width // 2 - final_score_text.get_width() // 2, screen_height // 2 - final_score_text.get_height() // 2))
    pygame.display.flip()

def draw_play_again_button():
    play_again_text = font_instruction.render("Play Again", True, white)
    play_again_rect = play_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    pygame.draw.rect(screen, violet, (play_again_rect.x - 10, play_again_rect.y - 10, play_again_rect.width + 20, play_again_rect.height + 20))
    screen.blit(play_again_text, play_again_rect)
    pygame.display.flip()

    return play_again_rect

def get_user_answer(choices):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, choice in enumerate(choices):
                    text_rect = font_instruction.render(f"{chr(65 + i)}. {choice}", True, violet).get_rect(center=(screen_width // 2, screen_height // 2 - len(choices) * 25 + i * 50))
                    if text_rect.collidepoint(x, y):
                        return choices[i]

def main():
    global screen, clock
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Guess the Song Game")

    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)

    total_levels = 3
    rounds_per_level = 3
    total_score = 0
    lives = 3

    # Durations for each level
    level_durations = [15, 10, 5]

    while True:  # Loop for replaying the game
        level = 1
        round_num = 1

        draw_play_button('img/Background.png')

        play_button_rect = font_instruction.render("Play", True, white).get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        play_button_clicked = False

        while not play_button_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if play_button_rect.collidepoint(x, y):
                        play_button_clicked = True

        draw_blank_background()

        while level <= total_levels:  # Outer loop for levels

            # Shuffle the songs for the current level
            all_songs = get_choices()
            random.shuffle(all_songs)
            song_index = 0

            while round_num <= rounds_per_level:  # Inner loop for rounds
                # Check if the player has lives remaining
                if lives == 0:
                    draw_final_score(total_score, 'img/Inner-Back.png')
                    speak("Game Over! You ran out of lives.")
                    play_again_rect = draw_play_again_button()

                    # Wait for the "Play Again" button to be clicked
                    play_again_clicked = False
                    while not play_again_clicked:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = event.pos
                                if play_again_rect.collidepoint(x, y):
                                    play_again_clicked = True

                    # Reset variables for a new game
                    total_score = 0
                    lives = 3
                    level = 1
                    round_num = 1
                    all_songs = get_choices()
                    random.shuffle(all_songs)
                    draw_blank_background()

                # Use the current song and move to the next one for the next round
                current_song = all_songs[song_index]
                song_index += 1

                # Create a list of choices with the correct answer and two incorrect answers
                choices = [current_song]
                for _ in range(2):
                    random_choice = random.choice(all_songs)
                    while random_choice in choices:
                        random_choice = random.choice(all_songs)
                    choices.append(random_choice)

                # Shuffle the choices so that the correct answer is in a random position
                random.shuffle(choices)

                draw_title('img/Inner-Back.png')
                time.sleep(1)

                speak(
                    f"Level {level}, Round {round_num}. Listen to the song. You have {level_durations[level - 1]} seconds to identify the correct one.")
                play_song(os.path.join("music", current_song + ".mp3"), level_durations[level - 1])

                # Set the duration for each round
                choice_timer_duration = level_durations[level - 1] * 1000

                choice_timer = pygame.time.get_ticks()

                # Update the display once per frame
                draw_choices_with_lives(choices, None, level, round_num, total_score,
                                        total_levels * rounds_per_level - (level - 1) * rounds_per_level - round_num, lives,
                                        'img/Inner-Back.png', choice_timer, choice_timer_duration)

                # Wait for the user to make a choice or time runs out
                timer_running = True
                user_answer = None
                while timer_running:
                    pygame.time.Clock().tick(30)

                    # Check if time ran out
                    if pygame.time.get_ticks() - choice_timer >= choice_timer_duration:
                        speak("Time's up! You didn't make a choice. To move on to the next round, you need to answer.")
                        lives -= 1  # Decrease lives when time runs out
                        timer_running = False
                        break

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            for i, choice in enumerate(choices):
                                text_rect = font_instruction.render(f"{chr(65 + i)}. {choice}", True, violet).get_rect(
                                    center=(screen_width // 2, screen_height // 2 - len(choices) * 25 + i * 50))
                                if text_rect.collidepoint(x, y):
                                    user_answer = choices[i]
                                    timer_running = False

                    # Update the display once per frame
                    draw_choices_with_lives(choices, None, level, round_num, total_score,
                                            total_levels * rounds_per_level - (level - 1) * rounds_per_level - round_num, lives,
                                            'img/Inner-Back.png', choice_timer, choice_timer_duration)

                # Check the user's answer if a choice was made
                if user_answer is not None:
                    if user_answer == current_song:
                        speak("Your guess is correct!")
                        total_score += 1
                    else:
                        correct_answer = [choice for choice in choices if choice == current_song][0]
                        speak(f"Sorry, your guess is incorrect. The correct answer is {correct_answer}.")
                        lives -= 1  # Decrease lives on incorrect answer

                    round_num += 1

            round_num = 1

            level += 1

        draw_final_score(total_score, 'img/Inner-Back.png')

        # Speak the final score
        speak(f"Your total score is {total_score} out of {total_levels * rounds_per_level}.")

        # Speak a perfect score message
        if total_score == total_levels * rounds_per_level:
            speak("Congratulations! You got a perfect score!")

        play_again_rect = draw_play_again_button()

        # Wait for the "Play Again" button to be clicked
        play_again_clicked = False
        while not play_again_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if play_again_rect.collidepoint(x, y):
                        play_again_clicked = True

        # Reset variables for a new game
        total_score = 0
        lives = 3
        all_songs = get_choices()
        random.shuffle(all_songs)
        song_index = 0
        round_num += 1
        level += 1
        round_num = 1
        draw_blank_background()

        pygame.display.flip()  # Update the display once per frame

if __name__ == "__main__":
    main()