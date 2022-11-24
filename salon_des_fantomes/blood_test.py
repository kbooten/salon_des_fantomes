## return a string describing the current psychointoxication of characters
## what does a blood test result look like?
import persons
all_characters = persons.get_people()


def blood_test_text(characters):
    text = " *<Toxicology results:>*\n"
    for char in characters:
        if len(char.psychotropics)==0:
            text.append("    *profile normal*\n")
        else:
            for psy in char.psychotropics:
                text.append("    *%s: %s parts per million*\n")
    return text


def main():


if __name__ == '__main__':
	main()