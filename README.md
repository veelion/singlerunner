singlerunner - Make sure there is only one instance running at the same time'
====================================
SingleRunner makes sure only one instance of programme running at the same time.
the programme most likes:
    1. it would run very long or run forever in a loop
    2. and more running at the same time would make something terribly bad

so, use SingleRunner like this:



    def my_main(a=1, b=3):
        import time
        while 1:
            print a+b
            a += 1
            b += 1

    import siglerunner

    sr = siglerunner.SingleRunner(__file__)
    as_daemon = False
    sr.run(as_daemon, my_main, 2,2)
    #sr.run(as_daemon, my_main, a=3, b=3)

