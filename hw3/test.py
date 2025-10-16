def main():
    g = None  # equivalent to 'g: integer'

    def B(a):
        x = None

        def A(val):
            nonlocal g
            g = val  # assigns to the variable g from the enclosing main()

        def R(m):
            nonlocal x
            print(x)
            x //= 2  # integer division
            if x > 1:
                R(m + 2)
            else:
                A(m + 1)

        x = a * a
        R(1)

    B(3)
    print(g)


if __name__ == "__main__":
    main()
