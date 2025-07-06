original_examples = """
    **Example 1 :**

      Commit Informations:
      - Hash (unique identifier): 1a2b3c4d
      - Author: John Doe
      - Date: 2025-01-01 10:00:00
      - Commit Message: Refactored the user authentication module to improve performance and readability.
      - Changed Files: auth.py, user_model.py
      - Diffs:
        auth.py:
        ```diff
        - def authenticate_user(username, password):
        -     if username and password:
        -         return check_credentials(username, password)
        + def authenticate_user(user_credentials):
        +     return validate_user(user_credentials)
      user_model.py:
      + def validate_user(credentials):
      +     # New validation logic for login
      +     return is_valid(credentials)
      **category**: Refactoring

      **Example 2 :**
      Commit Informations:
      - Hash (unique identifier): 3c2b1a4f
      - Author: Alex Brown
      - Date: 2025-01-03 12:00:00
      - Commit Message: Updated the README with installation instructions and new feature descriptions.
      - Changed Files: README.md
      - Diffs:
      README.md:
      ```diff
      + ## Installation
      + Run the following command to install:
      + pip install mypackage
      **category**: Documentation Update

      **Example 3 : **
      Commit Informations:
      - Hash (unique identifier): 9f8e7d6c
      - Author: Jane Smith
      - Date: 2025-01-02 15:00:00
      - Commit Message: Fixed incorrect handling of null values in user profile updates.
      - Changed Files: profile.py
      - Diffs:
      profile.py:
      ```diff
      - if user['name']:
      + if user.get('name') is not None:
      **category**: Bug Fix
"""

refined_examples = """
      **Example 1 :**

      Commit Informations:
      - Hash (unique identifier): 294a803552de8874390bedd5e3ce1ead703394c1
      - Author: Tor Andersson
      - Date: 2013-12-27 15:41:59
      - Commit Message: Print error message with line number on lexical errors.
      - Changed Files: js-lex.c, js-load.c, js.h
      - Diffs:
        js-lex.c:
        ```diff
        -js_Token js_syntaxerror(js_State *J, const char *fmt, ...)
        -{
        -    va_list ap;
        -    fprintf(stderr, 'syntax error: line %d: ', J->yyline);
        -    va_start(ap, fmt);
        -    vfprintf(stderr, fmt, ap);
        -    va_end(ap);
        -    fprintf(stderr, '\n');
        -    return JS_ERROR;
        -}
        -
        -            return js_syntaxerror(J, '0x not followed by hexademical digit');
        +            return JS_ERROR;
        -    if ((*sp)[0] == '0' && isdec((*sp)[1]))
        -            return js_syntaxerror(J, 'number with leading zero');
        +    if ((*sp)[0] == '0' && (*sp)[1] == '0')
        +            return JS_ERROR;
        -            return js_syntaxerror(J, 'number with letter suffix');
        +            return JS_ERROR;
        -            return js_syntaxerror(J, 'string not terminated');
        +            return JS_ERROR;
        -            return js_syntaxerror(J, 'regular expression not terminated');
        +            return JS_ERROR;
        -                    return js_syntaxerror(J, 'regular expression not terminated');
        +                    return JS_ERROR;
        -        else return js_syntaxerror(J, 'illegal flag in regular expression: %c', c);
        +        else return JS_ERROR;
        -        return js_syntaxerror(J, 'duplicated flag in regular expression');
        +        return JS_ERROR;
        -        if (isnewline(c)) {
        -            /* consume CR LF as one unit */
        -            if (c == '\r' && PEEK() == '\n')
        -                    NEXT();
        -            J->yyline++;
        +        if (isnewline(c))
        -        }
        -                    return js_syntaxerror(J, 'multi-line comment not terminated');
        +                    return JS_ERROR;
        -
        -void js_initlex(js_State *J)
        -{
        -    J->yyline = 1;
        -    J->lasttoken = JS_ERROR;
        -}
        ```
        js-load.c:
        ```diff
        -    js_initlex(J);
        ```
        js.h:
        ```diff
        -    int yyline;
        -void js_initlex(js_State *J);
        -js_Token js_syntaxerror(js_State *J, const char *fmt, ...);
        ```
      **category**: Feature Update



      **Example 2 :**

      Commit Informations:
      - Hash (unique identifier): f323d6a9717496be399b9306b2baa8ac1c5707a3
      - Author: Tor Andersson
      - Date: 2013-12-23 22:54:14
      - Commit Message: Clean up lexing macro use.
      - Changed Files: js-lex.c
      - Diffs:
        js-lex.c:
        ```diff
        -#define UNGET() (*sp)--
        -
        -#define GET() *(*sp)++
        -#define PEEK() (**sp)
        -#define NEXT() ((*sp)++)
        -#define NEXTPEEK() (NEXT(), PEEK())
        -#define LOOK(x) (PEEK() == x ? (NEXT(), 1) : 0)
        -
        +#define GETC() *(*sp)++
        +#define UNGETC() (*sp)--
        +#define LOOK(x) (**sp == x ? *(*sp)++ : 0)
        +
        -    int c = PEEK();
        -    while (c && !isnewline(c)) {
        -            c = NEXTPEEK();
        -    }
        +    int c = GETC();
        +    while (!isnewline(c))
        +            c = GETC();
        +    UNGETC();
        -
        -            int c = GET();
        +            int c = GETC();
        -
        -                    c = GET();
        +                    c = GETC();
        -static inline double lexhex(const char **sp)
        +static inline js_Token lexhex(const char **sp, double *yynumber)
        +    int c = GETC();
        -
        -    int c = PEEK();
        -    while (ishex(c)) {
        +    
        +    if (!ishex(c))
        +            return JS_ERROR;
        +    
        +    do {
        -            c = NEXTPEEK();
        -    }
        -    return n;
        +            c = GETC();
        +    } while (ishex(c));
        +    
        +    UNGETC();
        +    *yynumber = n;
        +    
        +    return JS_NUMBER;
        +    int c = GETC();
        -
        -    int c = PEEK();
        +    
        -            c = NEXTPEEK();
        +            c = GETC();
        +    
        +    UNGETC();
        +    
        +    int c = GETC();
        -
        -    int c = PEEK();
        +    
        -            c = NEXTPEEK();
        +            c = GETC();
        +    
        +    UNGETC();
        +    
        -static inline double lexexponent(const char **sp)
        +static inline js_Token lexnumber(int c, const char **sp, double *yynumber)
        -
        -    if (LOOK('e') || LOOK('E')) {
        -            if (LOOK('-'))
        -                    return -lexinteger(sp);
        -            else if (LOOK('+'))
        -                    return lexinteger(sp);
        -            else
        -                    return lexinteger(sp);
        -    }
        -    return 0;
        -}
        +    double i, f, e;
        -static inline js_Token lexnumber(const char **sp, double *yynumber)
        -{
        -    double n;
        +    if (c == '0' && (LOOK('x') || LOOK('X')))
        +            return lexhex(sp, yynumber);
        -
        -    if ((*sp)[0] == '0' && ((*sp)[1] == 'x' || (*sp)[1] == 'X')) {
        -            *sp += 2;
        -            if (!ishex(PEEK()))
        -                    return JS_ERROR;
        -            *yynumber = lexhex(sp);
        -            return JS_NUMBER;
        -    }
        +    UNGETC();
        -
        -    if ((*sp)[0] == '0' && (*sp)[1] == '0')
        -            return JS_ERROR;
        +    i = lexinteger(sp);
        -
        -    n = lexinteger(sp);
        +    f = 0;
        -            n += lexfraction(sp);
        -    n *= pow(10, lexexponent(sp));
        +            f = lexfraction(sp);
        -
        -    if (isidentifierstart(PEEK()))
        -            return JS_ERROR;
        +    e = 0;
        +    if (LOOK('e') || LOOK('E')) {
        +            if (LOOK('-'))
        +                    e = -lexinteger(sp);
        +            else if (LOOK('+'))
        +                    e = lexinteger(sp);
        +            else
        +                    e = lexinteger(sp);
        +    }
        +    
        +    *yynumber = (i + f) * pow(10, e);
        -
        -    *yynumber = n;
        -    int c = GET();
        +    int c = GETC();
        -
        -            x = tohex(GET());
        -            y = tohex(GET());
        -            z = tohex(GET());
        -            w = tohex(GET());
        +            x = tohex(GETC());
        +            y = tohex(GETC());
        +            z = tohex(GETC());
        +            w = tohex(GETC());
        -
        -            x = tohex(GET());
        -            y = tohex(GET());
        +            x = tohex(GETC());
        +            y = tohex(GETC());
        -
        -    int c = GET();
        +    int c = GETC();
        -
        -            c = GET();
        +            c = GETC();
        -
        -    int c = GET();
        +    int c = GETC();
        +    
        -                    c = GET();
        +                    c = GETC();
        -
        -                    if (LOOK('/')) {
        +                    c = GETC();
        +                    if (c == '/') {
        -                    } else if (LOOK('*')) {
        +                    } else if (c == '*') {
        -                    } else if (LOOK('=')) {
        +                    } else if (c == '=') {
        +                            UNGETC();
        -
        -            *p++ = c;
        -
        -            c = PEEK();
        -            while (isidentifierpart(c)) {
        +            do {
        -                    c = NEXTPEEK();
        -            }
        +                    c = GETC();
        +            } while (isidentifierpart(c));
        +            UNGETC();
        -
        -            if (c == '.') {
        -                    if (isdec(PEEK())) {
        -                            UNGET();
        -                            return lexnumber(sp, yynumber);
        -                    }
        -                    return JS_PERIOD;
        -            }
        -
        -            if (c >= '0' && c <= '9') {
        -                    UNGET();
        -                    return lexnumber(sp, yynumber);
        -            }
        +            if ((c >= '0' && c <= '9') || c == '.')
        +                    return lexnumber(c, sp, yynumber);
        -
        -            c = GET();
        +            c = GETC();
        ```
      **category**: Refactoring



      **Example 3 :**

      Commit Informations:
      - Hash (unique identifier): e01fe424ab94395713d94f46eee57f1af0a279b4
      - Author: Tor Andersson
      - Date: 2013-12-27 17:33:04
      - Commit Message: Check hex string escapes so we don't read past the end of the string.
      - Changed Files: js-lex.c
      - Diffs:
        js-lex.c:
        ```diff
        -    int x = 0;
        +    int x, y, z, w;
        -            if (!ishex(PEEK())) return x; else x |= NEXTPEEK() << 12;
        -            if (!ishex(PEEK())) return x; else x |= NEXTPEEK() << 8;
        -            if (!ishex(PEEK())) return x; else x |= NEXTPEEK() << 4;
        -            if (!ishex(PEEK())) return x; else x |= NEXTPEEK(); 
        -            return x;
        +            x = tohex(GET());
        +            y = tohex(GET());
        +            z = tohex(GET());
        +            w = tohex(GET());
        +            return (x << 12) | (y << 8) | (z << 4) | w;
        -            if (!ishex(PEEK())) return x; else x |= NEXTPEEK() << 4;
        -            if (!ishex(PEEK())) return x; else x |= NEXTPEEK();
        -            return x;
        +            x = tohex(GET());
        +            y = tohex(GET());
        +            return (x << 4) | y;
        ```
      **category**: Bug Fix


    **Example 4 :**
    
    Commit Informations:
    
    * Hash (unique identifier): 24e9127b836736fc4c3abdb6398e9848f1b27ae8
    * Author: Tor Andersson
    * Date: 2014-01-10 11:12:18
    * Commit Message: Style cleanup.
    * Changed Files: js-ast.c, js-ast.h, js-lex.c, js-parse.c, js.h
    * Diffs:
      js-ast.c:
    
    ```diff
    -    case EXP_VAR: return "VAR";
    +    case AST_INIT: return "INIT";
    @@
    -    case EXP_VAR:
    +    case AST_INIT:
             printast(n->a, level);
             if (n->b) {
    -            printf(" = ");
    +            printf(" = ");
                 printast(n->b, level);
             }
    ```
    
    js-parse.c:
    
    ```diff
    -#define TOKSTR        jsP_tokenstring(J->lookahead)
    +#define A1(x,a)       jsP_newnode(J, x, a, 0, 0, 0)
    +#define A2(x,a,b)     jsP_newnode(J, x, a, b, 0, 0)
    +#define A3(x,a,b,c)   jsP_newnode(J, x, a, b, c, 0)
    ```
    
    js.h:
    
    ```diff
    -const char *jsP_tokenstring(int token);
    ```
    
    **category**: Style Update
    
    ---
    
    **Example 5 :**
    
    Commit Informations:
    
    * Hash (unique identifier): effc3ae9ad351c53f4b3ecba8669464e4a97c8c2
    * Author: Tor Andersson
    * Date: 2014-01-10 14:34:27
    * Commit Message: Add constant folding.
    * Changed Files: jsload.c, jsoptim.c, jsparse.c, jsparse.h, jspretty.c
    * Diffs:
      jsoptim.c (new file - extracted part):
    
    ```diff
    +static inline int i32(double d) { /* … */ }
    +static inline unsigned int u32(double d) { return i32(d); }
    +
    +static int foldnumber(js_Ast *node, double *r) {
    +    /* recursively traverses the AST and replaces
    + constant arithmetic expressions with a single number node */
    +    if (node->a && node->b) {
    +        switch (node->type) {
    +        case EXP_MUL: return N(node, r, x * y);
    +        case EXP_ADD: return N(node, r, x + y);
    +        /* other operations … */
    +        }
    +    }
    +    /* … */
    +}
    +
    +void jsP_foldconstants(js_State *J, js_Ast *prog) {
    +    double x;
    +    foldnumber(prog, &x);
    +}
    ```
    
    jsload.c (extracted):
    
    ```diff
    -        jsP_foldconstants(J, prog);
    ```
    
    jsparse.c (related part):
    
    ```diff
    +    /* after parsing, perform constant folding */
    +    jsP_foldconstants(J, prog);
    ```
    
    **category**: Performance Improvement 
    
    **Example 6 :**

      Commit Informations:
      - Hash (unique identifier): 50d5cb95abc045d219fa80e9b1f41470e2d86a89
      - Author: Tor Andersson
      - Date: 2014-01-12 12:50:39
      - Commit Message: Auto-generate list of operator names.
      - Changed Files: Makefile, jsdump.c
      - Diffs:
        Makefile:
        ```diff
        -opnames.h : jscompile.h
        -	grep 'OP_' jscompile.h | sed 's/OP_/\"\"/;s/,/\"\",/' | tr A-Z a-z > opnames.h
        -
        -jsdump.c : opnames.h
        +opnames.h : jscompile.h
        +	# auto-genera opnames.h a partire dagli opcode definiti
        +	grep 'OP_' jscompile.h | sed 's/OP_/\"\"/;s/,/\"\",/' | tr A-Z a-z > opnames.h
        +
        +jsdump.c : opnames.h
        ```
      **category**: Build/CI Change



    **Example 7 :**

      Commit Informations:
      - Hash (unique identifier): 7f3673fee2f872d78c3ffad3c50ee7196f2a5862
      - Author: Tor Andersson
      - Date: 2014-01-12 14:11:08
      - Commit Message: Document some trickier byte codes.
      - Changed Files: jscompile.c, jscompile.h, Makefile
      - Diffs:
        jscompile.c:
        ```diff
        -    emit(J, F, OP_LOAD);
        +    // Duplicates the address and loads the value in a single step
        +    emit(J, F, OP_DUP_LOAD);
        ```
        jscompile.h:
        ```diff
        -    OP_LOAD,  /* <addr> -- <addr> <value> */
        +    OP_LOAD,      /* <addr> -> <addr> <value> */
        +    OP_DUP_LOAD,  /* <addr> duplicate + load in a single step */
        ```
      **category**: Documentation Update   
"""


refined_ex = """
    **Ecco dieci esempi “migliorati” riferiti al repository *mujs*.
Ogni esempio è in C, mantiene esattamente i campi richiesti e copre una sola categoria.**

---

### **Example 1 :**

Commit Informations:

* **Hash (unique identifier):** 47ea2b1c
* **Author:** Aki Hara
* **Date:** 2025-01-04 09:12:43
* **Commit Message:** Added preliminary BigInt support to the VM and value API.
* **Changed Files:** jsbigint.c, jsbigint.h, vm.c
* **Diffs:**
  jsbigint.c:

  ```diff
  +typedef struct js_BigInt {
  +    int sign;
  +    uint32_t *limbs;
  +    size_t    nlimbs;
  +} js_BigInt;
  +
  +js_BigInt *js_newbigint(js_State *J, int64_t v);
  ```

  vm.c:

  ```diff
  -case JS_TNUMBER:
  +case JS_TBIGINT:
  +    /* fall through */
  +case JS_TNUMBER:
  ```

**category**: Feature Update

---

### **Example 2 :**

Commit Informations:

* **Hash (unique identifier):** b62dca4e
* **Author:** Paolo Rossi
* **Date:** 2025-01-05 16:27:08
* **Commit Message:** Fix crash on empty character class in RegExp parser.
* **Changed Files:** regexp.c
* **Diffs:**
  regexp.c:

  ```diff
  -if (*p == ']') error(J, "unterminated character class");
  +if (*p == ']' && p == class_start + 1)
  +    error(J, "empty character class");
  ```

**category**: Bug Fix

---

### **Example 3 :**

Commit Informations:

* **Hash (unique identifier):** 9051f0e9
* **Author:** Mei Ling
* **Date:** 2025-01-06 11:02:31
* **Commit Message:** Expanded README with build instructions for Windows/MSVC.
* **Changed Files:** README.md
* **Diffs:**
  README.md:

  ````diff
  +### Building on Windows (MSVC)
  +```cmd
  +cmake -G "Visual Studio 17 2022" -B build
  +cmake --build build --config Release
  +```
  ````

**category**: Documentation Update

---

### **Example 4 :**

Commit Informations:

* **Hash (unique identifier):** 3f09d8a7
* **Author:** Lilian Agosti
* **Date:** 2025-01-07 14:45:12
* **Commit Message:** Split garbage-collector into gc.c / gc\\_sweep.c for clarity.
* **Changed Files:** gc.c (removed), gc\\_mark.c (renamed), gc\\_sweep.c (new)
* **Diffs:**
  gc\\_mark.c:

  ```diff
  -static void gc_run(js_State *J) {
  -    mark_roots(J);
  -    sweep(J);
  -}
  +static void gc_mark(js_State *J) {
  +    mark_roots(J);
  +}
  ```

  gc\\_sweep.c:

  ```diff
  +static void gc_sweep(js_State *J) {
  +    /* new sweep implementation */
  +}
  ```

**category**: Refactoring

---

### **Example 5 :**

Commit Informations:

* **Hash (unique identifier):** 1cf782d4
* **Author:** Samuel Grey
* **Date:** 2025-01-08 18:59:55
* **Commit Message:** Optimised property lookup with cached hash → \\~18 % speed-up in benchmarks.
* **Changed Files:** jsobject.c, jsobject.h
* **Diffs:**
  jsobject.c:

  ```diff
  -for (prop = obj->props; prop; prop = prop->next)
  -    if (js_strcmp(atom, prop->name) == 0) return prop;
  +uint32_t h = js_hash(atom);
  +prop = obj->buckets[h & (BUCKETS - 1)];
  +while (prop && prop->name != atom) prop = prop->next;
  +return prop;
  ```

**category**: Performance Improvement

---

### **Example 6 :**

Commit Informations:

* **Hash (unique identifier):** e4d7b0c2
* **Author:** Ingrid Cho
* **Date:** 2025-01-09 10:13:20
* **Commit Message:** Added Promise conformance tests from Test262 subset.
* **Changed Files:** tests/promise\\_test.c, Makefile
* **Diffs:**
  promise\\_test.c:

  ```diff
  +TEST(test_resolve_reject) {
  +    js_pushglobal(J);
  +    js_dostring(J, "new Promise(r => r(42)).then(v => assert(v===42));");
  +}
  ```

**category**: Test Addition/Update

---

### **Example 7 :**

Commit Informations:

* **Hash (unique identifier):** 58e556aa
* **Author:** Lucas Martins
* **Date:** 2025-01-10 13:51:02
* **Commit Message:** Update Unicode data tables to 15.1 and regenerate unicodedata.c.
* **Changed Files:** unicodedata.c, scripts/gen\\_unicode.py
* **Diffs:**
  unicodedata.c:

  ```diff
  -/* UnicodeVersion: 14.0 */
  +/* UnicodeVersion: 15.1 */
  ```

**category**: Dependency Update

---

### **Example 8 :**

Commit Informations:

* **Hash (unique identifier):** a1d0b6e3
* **Author:** Sofia Herrera
* **Date:** 2025-01-11 08:05:44
* **Commit Message:** Add GitHub Actions workflow for Linux/macOS builds & tests.
* **Changed Files:** .github/workflows/ci.yml
* **Diffs:**
  ci.yml:

  ```diff
  +runs-on: ${{ matrix.os }}
  +strategy:
  +  matrix:
  +    os: [ubuntu-latest, macos-latest]
  ```

**category**: Build/CI Change

---

### **Example 9 :**

Commit Informations:

* **Hash (unique identifier):** d95f7260
* **Author:** Elena Šimunović
* **Date:** 2025-01-12 17:36:18
* **Commit Message:** Apply clang-format (LLVM preset) across entire code-base.
* **Changed Files:** \\* (51 files)
* **Diffs:**
  jsrun.c:

  ```diff
  -if(argc<2){printf("usage: %s file.js\n",argv[0]);return 1;}
  +if (argc < 2) {
  +    printf("usage: %s file.js\n", argv[0]);
  +    return 1;
  +}
  ```

**category**: Style Update

---

### **Example 10 :**

Commit Informations:

* **Hash (unique identifier):** 2e4af883
* **Author:** Omar El-Sayed
* **Date:** 2025-01-13 12:21:09
* **Commit Message:** Add .gitattributes to enforce LF line endings for C sources.
* **Changed Files:** .gitattributes
* **Diffs:**
  .gitattributes:

  ```diff
  +*.c text eol=lf
  +*.h text eol=lf
  ```

**category**: Other

"""