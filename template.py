import sys

def template(file, outfile = None):
    outfile = outfile if outfile else file
    with open(file, "r") as f:
        contents = f.read()
    with open(outfile, "w") as f:
        inTemplate = False
        templateStr = ""
        i = 0
        while i < len(contents):
            try:
                side = ["{{", "}}"].index(contents[i:i+2])
                inTemplate = side == 0
                if inTemplate:
                    templateStr = ""
                else:
                    try:
                        with open(templateStr, "r") as templateContent:
                            f.write(templateContent.read())
                    except FileNotFoundError:
                        templateStr = "{{" + templateStr + "}}"
                        print("Could not fill template",templateStr)
                        f.write(templateStr)
                i += 2
            except ValueError:
                if inTemplate and not contents[i].isspace():
                    templateStr += contents[i]
                else:
                    f.write(contents[i])
                i += 1

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <templateFile> <outfile>")
        exit(1)

    template(*sys.argv[1:])

if __name__ == "__main__":
    main()
