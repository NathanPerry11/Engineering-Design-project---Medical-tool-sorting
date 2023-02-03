#!/usr/bin/env python
# coding: utf-8

# In[2]:



    


def identify_autoclave_bin_location(i_d): #Function by Grayson
    green_small = [0, -.629, 0.47]        #Set of coordinates corresponding to each drop off location 
    red_small = [-0.588, 0.238, 0.435] 
    blue_small = [0, 0.634, 0.435] 
    green_large = [0, -0.421, 0.364] 
    blue_large= [0, 0.421, 0.364] 
    red_large = [-0.386, 0.156, 0.35] 
    if i_d == 4:
        bin_location = [red_large[0], red_large[1], red_large[2]]        #Depending on the ID number, assign the corresponding 
                                                                        #set of coordinates to a variable which will be passed
    elif i_d == 6:                                                      #through the move arm function and move it to the correct
        bin_location = [blue_large[0], blue_large[1], blue_large[2]]    #drop off location
       
    elif i_d == 5:
        bin_location = [green_large[0], green_large[1], green_large[2]]
       
    elif i_d == 1:
        bin_location = [red_small[0], red_small[1], red_small[2]]
       
    elif i_d == 3:
        bin_location = [blue_small[0], blue_small[1], blue_small[2]]
        
    elif i_d == 2:
        bin_location = [green_small[0], green_small[1], green_small[2]]
       
    return bin_location
            
     

def open_autoclave_bin_drawer(i_d,container_closed):      #Function by both team members
    while True:                                                           
        if (arm.emg_left()>.75) and (arm.emg_right()==0):  #Infinite while loop until left arm is flexed to a threshold of .75 and right arm is not flexed
            if container_closed:                           #container_closed is a boolean which is passed through the function
                if i_d == 4:                               #and determines whether the autoclave needs to be opened or closed
                    arm.open_red_autoclave(True)           #True is open and vice versa. Based on the ID number, the function
                    break                                  #opens or closes the correct autoclave drawer
        
                elif i_d == 6: 
                    arm.open_blue_autoclave(True)
                    break
        
                elif i_d == 5: 
                    arm.open_green_autoclave(True)
                    break
            else:
                if i_d == 4:
                    arm.open_red_autoclave(False)
                    break
        
                elif i_d == 6: 
                    arm.open_blue_autoclave(False)
                    break
        
                elif i_d == 5: 
                    arm.open_green_autoclave(False)
                    break



def close_gripper(gripper_open):   #Function by Nathan #If both arms are flexed past a threshold of .75, open or close the gripper
                                                       #the direction the gripper moves depends on whether True or False is
    while True:                                        #passed through the function 
        if (arm.emg_right()>.75) and (arm.emg_left()>.75):
            if (gripper_open):
                arm.control_gripper(30)
                break
            else:
                arm.control_gripper(-30)
                break
          
               

def move_q_arm(bin_location):    #Function by Nathan   #If the right arm is flexed past a threshold of .75 and the left is not flexed, move the arm to the coordinates that
    while True:                                       #are passed through the function 
        if (arm.emg_right()>.75) and (arm.emg_left()==0): 
            arm.move_arm(bin_location[0],bin_location[1],bin_location[2])
            break

def main_func(): #Function by both team members
    import random
    g_s=False #Booleans that determine whether each container ID has been sorted (g_s corresponds to green_small etc...)
    r_s=False 
    b_s=False
    g_l=False
    r_l=False
    b_l=False
    
    while True:                        #While loop repeats function until all six containers have been sorted
        while True:
            i_d=random.randint(1,6)      #Randomly generates an integer that determines ID number
            
            if (i_d==1) and (r_s==False): #Changes the boolean to true everytime a specific ID is chosen, letting the arm know
                r_s=True                  #which containers have already been sorted
                break      
            elif (i_d==2) and (g_s==False):
                g_s=True
                break
            elif (i_d==3) and b_s==False:
                b_s=True
                break
            elif (i_d==4) and (g_l==False):
                g_l=True
                break
            elif i_d==5 and (r_l==False):
                r_l=True
                break
            elif (i_d==6) and (b_l==False):
                b_l=True
                break                         #While loop only lets the ID be run through the function if it has not been chosen yet
                                        
              
                
        arm.spawn_cage(i_d)  #Spawn a cage based on generated ID
        bin_location=((identify_autoclave_bin_location(i_d))) #Assign the bin location based on the ID number 
        move_q_arm([.534,0,0.044]) #Move the arm to the pickup location, this location never changes
        time.sleep(2)
        close_gripper(True)        #Move the gripper, passing true through it closes it
        time.sleep(2)
        move_q_arm(bin_location)   #Move the arm to the assigned bin coordinates
        time.sleep(2)
        if i_d>3:
            open_autoclave_bin_drawer(i_d,True) #Run the open autoclave function if the ID is greater than 3 (if it is large)
                                                #Passing true opens the autoclave
        time.sleep(2)
        close_gripper(False) #Move the gripper, passing false through it opens it 
        time.sleep(2)
        if i_d>3: 
            open_autoclave_bin_drawer(i_d,False) #Close the autoclave, this is only called if the container is large (ID>3)
        time.sleep(2)                            #Passing false closes the autoclave
        arm.home()  #Move the arm to the home position
        time.sleep(3)
       
    
        if (r_s==True) and (g_s==True) and (b_s==True) and (b_l==True) and (r_l==True) and (g_l==True): #If all six containers have been passed through, break the loop and terminate the arm
            arm.home()
            #arm.terminate_arm() #This would be called if we were in real life 
            break

