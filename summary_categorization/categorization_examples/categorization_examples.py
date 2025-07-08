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


refined_ex = """

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