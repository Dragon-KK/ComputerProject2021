

def main():
    failed = False
    try:
        import PIL
        print("PIL Successfully imported")
    except ImportError as e:
        print(e)
        print("Module PIL could not be imported")
        print("Try `pip install pillow`")
        failed = True

    if failed:
        print("Failed to import all dependencies")
    else:
        print("All dependencies are installed : )")
        

if __name__ == "__main__":
    main()