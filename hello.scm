;; HOWTO:
;;
;; Scheme program files are named SOMETHING.scm.
;;
;; Make it quiet:
;; $ export GUILE_AUTO_COMPILE=0
;;
;; Run w/ 0 arguments:
;; $ guile hello-world.scm
;;
;; Run w/ 1 argument:
;; $ guile hello-world.py Tau

(define (main argv)
  (if (= (length argv) 1)   ;; why 2?
    (display "Hello, STRANGER! \n")
    (display (string-append "Hello, " (list-ref argv 1) "! \n")))
  (exit 0))

(main (command-line))
