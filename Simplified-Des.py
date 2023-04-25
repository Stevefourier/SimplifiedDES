from collections import deque # Imported deque from the collections library to perform left and shift operations

#Hardwired permutation values according to Stallings

perm_8 = [6, 3, 7, 4, 8, 5, 10, 9]
perm_4 = [2, 4, 3, 1]
perm_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
initial_perm =[2, 6, 3, 1, 4, 8, 5, 7]
initial_perminv = [4, 1, 3, 5, 7, 2, 8, 6]
exp_permOp = [4, 1, 2, 3, 2, 3, 4, 1]

#Hardwired S-boxes
s_0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]] 
s_1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]] 
s1modified = [[2, 1, 0, 3], [2, 0, 1, 3], [3, 0, 1, 0], [0, 1, 2, 3]] # Modfied S1

# This functions converts 2-bit decimal value to binary

def twoBitCon(x):
	x = str(x)
	staticBin = ['0']
	if len(x) < 2:
		staticBin.append(x)
		return ''.join(staticBin)
	else:
		return x

#XOR function
def xor_op(x,y): 
	keyResult = []
	for element in range(len(x)):
		if x[element] == y[element]:
			keyResult.append(0)
		else:
			keyResult.append(1)
	return keyResult


#Function to generate keys K1 and K2 using the 10 bit key input

def genSubKey():
	key10Bit = input("Enter the 10-bit key: ")

	key10Bit = str(key10Bit)

	key10Bit_perm10 = []
	key8Bit_perm8 = []

	for number in range(len(key10Bit)):
		key10Bit_perm10.append(key10Bit[perm_10[number]-1])

	cirLeftkey10Bit_perm10 = key10Bit_perm10[:5]
	cirRightkey10Bit_perm10 = key10Bit_perm10[5:]

	#Performing a circular left shift by 1 for separately on the first five bits and the second five bits on the 10 bits input

	cirLeftkey10Bit_perm10Shift1 = deque(cirLeftkey10Bit_perm10)
	cirLeftkey10Bit_perm10Shift1.rotate(-1)
	cirRightkey10Bit_perm10Shift1 = deque(cirRightkey10Bit_perm10)
	cirRightkey10Bit_perm10Shift1.rotate(-1)

	#Merging two left and right key shifted by 1
	mergeLeftRight1 = list(cirLeftkey10Bit_perm10Shift1 + cirRightkey10Bit_perm10Shift1)

	#Applying P8, which picks out and permutes 8 of the 10 bits in the merge mergeLeftRight1 list to get the subkey K1

	for perm in range(len(perm_8)):
		key8Bit_perm8.append(mergeLeftRight1[perm_8[perm] - 1])
	Key1 = key8Bit_perm8

	#Splitting 10 bits in the merged list into two 5 bits
	mergeLeft = mergeLeftRight1[:5]
	mergeRight = mergeLeftRight1[5:]

	#Performing a circular left shift of 2 bit positions on each pair of 5-bit string produced by

	mergeLeft_Shift2 = deque(mergeLeft)
	mergeLeft_Shift2.rotate(-2)
	mergeRight_Shift2 = deque(mergeRight)
	mergeRight_Shift2.rotate(-2)

	#Merging the result of the circular left shift of 2 bit positions on each pair of 5-bit string (left and right) into a list
	mergeLeftRight2 = list(mergeLeft_Shift2 + mergeRight_Shift2)

	mergeLeftRight2_perm8 = [] #An empty list to store the result of effecting a permutation of 8 on mergeLeftRight2

	
	#Applying a permutation of 8 on mergeLeftRight2 to produce subkey K2
	for perm in range(len(perm_8)):
		mergeLeftRight2_perm8.append(mergeLeftRight2[perm_8[perm] - 1])
	Key2 = mergeLeftRight2_perm8

	return Key1, Key2

def processEnc(Key1, Key2, s_1, plainText, encText, outputText):
	#Empty list to store user input for 8-bit block of plaintext
	plaintextIP = []
	for i in range(len(initial_perm)):
		plaintextIP.append(plainText[initial_perm[i] - 1])

	#Splitting the 8-bit block into 4 bits each
	leftHalf = plaintextIP[:4]
	rightHalf = plaintextIP[4:]

	#Permutation of the right 4 bits by the expansion/permutation (E/P)
	rightEP = []
	for perm in range(len(exp_permOp)):

		rightEP.append(rightHalf[exp_permOp[perm] -1])

	#Performing a bit wise operation of right 4 bits permuatated with (E/P) 
	right_xor = xor_op(rightEP, Key1)
	
	#Indexing matrix from s-box SO and merging them
	r1 = right_xor[:4] 
	r2 = right_xor[4:] 
	r1_f = int(''.join([str(r1[0]), str(r1[-1])]), 2) 
	r1_s = int(''.join([str(r1[1]), str(r1[-2])]), 2) 
	r2_f = int(''.join([str(r2[0]), str(r2[-1])]), 2) 
	r2_s = int(''.join([str(r2[1]), str(r2[-2])]), 2) 
	s0_r1 = s_0[r1_f][r1_s] 
	s0_r1_b = twoBitCon("{0:b}".format(int(s0_r1)))
	s1_r2 = s_1[r2_f][r2_s] 
	s1_r2_b = twoBitCon("{0:b}".format(int(s1_r2))) 
	t = [s0_r1_b + s1_r2_b][0]

	#Permutation of merged index output with perm_4 
	s0_s1 = [] 
	for i in range(len(t)):
		s0_s1.append(t[i]) 

	s0_s1_perm4 = [] 
	for i in range(len(perm_4)):
		s0_s1_perm4.append(s0_s1[perm_4[i] - 1])
	s0_s1_perm4 


	# XOR left 4 bits with p4 
	L_R = xor_op(leftHalf, s0_s1_perm4) +  rightHalf
	L_R = [str(_) for _ in L_R] 

	# Splitting and switching output into Left and Right halves 
	leftResult = L_R[4:] 
	rightResult = L_R[:4]

	#Displaying the intermediate result after switching operation while encrypting and decrypting
	print(f"The intermediate result after switch operation while {encText}")
	print(f"Left bits involved is {''.join(leftResult)} and Right bits involved is {''.join(rightResult)}")

	#Permutation of the right half of the output gotten as a result of the switch operation with (E/P)

	right_ep = []
	for i in range(len(exp_permOp)):
		right_ep.append(rightResult[exp_permOp[i] - 1])

	#Performing a bit-by-bit exclusive-OR operation on the result of the previous permutation
	right_ep_xorKey2 = xor_op(right_ep, Key2)


	#Indexing matrix from S-box (Original S1 or modified S1) and combining them

	r_r1 = right_ep_xorKey2[:4]
	r_r2 = right_ep_xorKey2[4:] 
	r_r1 = [str(_) for _ in r_r1] 
	r_r2 = [str(_) for _ in r_r2] 
	r_r1_f = int(r_r1[0] + r_r1[-1], 2) 
	r_r1_s = int(r_r1[1] + r_r1[-2], 2) 

	r_r2_f = int(r_r2[0] + r_r2[-1], 2) 
	r_r2_s = int(r_r2[1] + r_r2[-2], 2) 

	r_s0_r1 = s_0[r_r1_f][r_r1_s] 
	r_s1_r2 = s_1[r_r2_f][r_r2_s] 

	r_s0_r1_b = twoBitCon("{0:b}".format(r_s0_r1)) 
	r_s1_r2_b = twoBitCon("{0:b}".format(r_s1_r2))

	#Merging and permutation with perm_4 which is P4 according to stallings
	s0_s1 = r_s0_r1_b + r_s1_r2_b
	s0_s1_pem4 = []
	for i in range(len(perm_4)):
		s0_s1_pem4.append(s0_s1[perm_4[i] - 1])

	#Performing a bit by bit exclusive-OR operation of the left half with previous result
	leftXor_s0_s1_perm4 = xor_op(s0_s1_pem4, leftResult)
	left_right_comp = [str(_) for _ in leftXor_s0_s1_perm4 + rightResult]

	#Storing cipher text
	cipherText = []
	for i in range(len(initial_perminv)):
		cipherText.append(left_right_comp[initial_perminv[i] - 1])
	output = '' .join(cipherText)


	print(f"{outputText} is {output}")
	return cipherText

#Display of the encryption and decryption intermedite process and output
#Part (a)
print("------------------------------------------------------------------------------------------------")
print("Question (a) : Computation with original S1                                                    |")
print("------------------------------------------------------------------------------------------------")
Key1, Key2 = genSubKey() 
plainText = input("Enter the 8 bit block plain text: ") 

#Encryption of plain text with S-box S0 and original S1 

cipherText = processEnc(Key1, Key2, s_1, plainText, 'encrypting', 'Cipher text') 
# Decryption of cipher text after encryption 
processEnc(Key2, Key1, s_1, cipherText, 'decrypting', 'Decryption result')
print()
#Part (b)
print("--------------------------------------------------------------------------------------------------")
print("Question (b): Computation with original S1: Plaintext is 11110110 and Key is 1011110110          |")
print("--------------------------------------------------------------------------------------------------")
Key1, Key2 = genSubKey() 
plainText = input("Input1: Enter the 8 bit block plain text: ") 

#Encryption of plain text with S-box S0 and original S1 
cipherText = processEnc(Key1, Key2, s_1, plainText, 'encrypting', 'Cipher text') 

#Decryption of cipher text after encryption 
processEnc(Key2, Key1, s_1, cipherText, 'decrypting', 'Decryption result')
print()

# Part (c) 
print("--------------------------------------------------------------------------------------------------")
print("Question (c) with modified S1                                                                    |") 
print("--------------------------------------------------------------------------------------------------")
Key1, Key2 = genSubKey() 
plainText = input("Enter the 8 bit block plain text: ") 

#Encryption of plain text with S-box S0 and modified S1 
cipherText = processEnc(Key1, Key2, s1modified, plainText, 'encrypting', 'Cipher text') 

# Decryption of cipher text derived previously 
processEnc(Key2, Key1, s1modified, cipherText, 'decrypting', 'Decryption result')












	
