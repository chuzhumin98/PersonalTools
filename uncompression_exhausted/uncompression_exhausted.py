path = 'xxx/xxx.rar' # your file path

import os


def nextPass(passidxs, m, N):
    passidxs[-1] += 1
    for i in range(m-1, 0, -1):
        if passidxs[i] >= N:
            passidxs[i] -= N
            passidxs[i-1] += 1
        else:
            break

    if passidxs[0] == N:
        return False
    return True

passset = 'abc123' # this is what you need to modify
N = len(passset)

is_success = False
success_pass = ''


cnt_try = 0
slice_output = 100
for i in range(1, 11):
    passidxs = [0] * i
    while True:
        password = ''.join([passset[_] for _ in passidxs])
        flag = os.system(f"echo {password} | unrar x {path} > /dev/null 2>&1") # fail: 65280 , success: 0; unrar is required
        cnt_try += 1
        if cnt_try % slice_output == 0:
            print(f'try {cnt_try} times with password = {password}')
        if flag == 0:
            is_success = True
            success_pass = password
            break

        if success_pass:
            break

        if not nextPass(passidxs, i, N):
            break


if is_success:
    print(f'password = {success_pass}!')
else:
    print('sorry, but not find the password!')




