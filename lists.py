import twl
import os

wolf = twl.Wolf()

if __name__ == "__main__":
    for n in range(2, 9):
        wolf.len(n).save("{}ltr.txt".format(n))

    two = wolf.len(2)

    for c in twl.vowels:
        two.hasltrs(c).save('2ltr_has_{}.txt'.format(c))

    two.len(2).notltrs(twl.vowels).save("2ltr_no_vowels.txt")

    wolf.smaller(8).vowel_count(0).save('no_vowels_under8.txt')
    wolf.smaller(8).notltrs(twl.vowels+'y').save('no_vowels_no_y_under8.txt')
    wolf.smaller(8).vowel_count(0).hasltrs('y').save('no_vowels_has_y_under8.txt')

    for n in range(2, 9):
        de = '{}ltr'.format(n)
        os.mkdir(de)
        os.chdir(de)
        num = wolf.len(n)
        num.save_by_letter(de)
        num.save_by_last_letter(de)
        os.chdir('..')
