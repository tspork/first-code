;; HOWTO:
;;
;; Scheme program files are named SOMETHING.scm.
;;
;; Make it quiet:
;; $ export GUILE_AUTO_COMPILE=0
;;
;; Run w/ 0 arguments:
;; $ guile hello.scm
;;
;; Run w/ 1 argument:
;; $ guile hello.py Tau

(define (main words)
  ;; (write words)(newline)(exit 0)
  (if (= (length words) 2)   ;; why 2?
    (display (string-append "Hello, " (list-ref words 1) "! \n"))
    (display "Hello, STRANGER! \n"))
  (exit 0))

(main (command-line))
