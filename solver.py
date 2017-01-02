from itertools import chain
import time
from selenium import webdriver


def get_solution(cube):
    cube_listed = []

    faces_listed = list(map(lambda x: list(chain.from_iterable(x)), cube))

    for i in range(3):
        for j in range(3):
            cube_listed.append(cube[5][2-j][i])

    cube_listed += faces_listed[3]
    cube_listed += faces_listed[0]
    cube_listed += faces_listed[1]
    cube_listed += faces_listed[2]

    for i in range(3):
        for j in range(3):
            cube_listed.append(cube[4][2-j][i])

    color_map = [3, 5, 1, 4, 2, 6]
    color_directions = ['F', 'B', 'U', 'R', 'L', 'D']


    cube_ruwix_string = ''.join(['0'] + list(map(lambda x: str(color_map[x]), cube_listed)))
    url = 'https://rubiks-cube-solver.com/solution.php?cube=' + cube_ruwix_string

    path_to_chromedriver = '/Users/markus/Tools/selenium_driver/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    browser.get(url)

    time.sleep(20)

    solution_steps = browser.find_element_by_xpath('//*[@id="segedvaltozo"]').text
    solution_steps = solution_steps[13:].split(' ')

    browser.close()

    current_orientation = (color_directions[cube[2][1][1]], color_directions[cube[4][1][1]])

    return (solution_steps, current_orientation)
