# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 11:08:54 2022

@author: kasimoglu
"""

import csv
import random
import numpy as np


class DoEPointGenerator():
    """Generate locally d-optimal DoE test points"""
    def __init__(self):
        super().__init__()
   
    def get_variable_name(self,parent):
        """Initial variable names etc. is taken from here"""
        self.variable_names = [
            "Step",
            "Variable1",
            "Variable2",
            "Variable3",
            "Variable4",
            "Time"
            ]        
        return self.variable_names
    def generate_doe_points(self, sample_space_boundry_list, num_of_steps, 
                            num_of_var, sel_model, num_of_iter):
        """Generation of DoE points.
        
        Boundaries of sample space, num of test steps, selected model, number 
        of iteration etc. is taken and based on the maximization of determinant
        of X'X d-optimal test points are selected.
        
        Here X is information matrix which is constructed upon the selected 
        model. Model is something like AX**2 + BXY + ... X' is transpose of 
        information matrix. 
        """
        self.doe_variables = []
        self.sample_spc_bndry = []
        
        # Model için sınır değişkeni isimleri ve mak. min değerleri alınır
        for i in range(len(sample_space_boundry_list)//3):

            self.doe_variables.append(sample_space_boundry_list[i*3])
            self.sample_spc_bndry.append(sample_space_boundry_list[(i*3)+1])
            self.sample_spc_bndry.append(sample_space_boundry_list[(3*i)+2])

        # Sample space boundary points are scaled between -1 and 1
        self.scaled_sample_spc_bndry = []
        for i in range(len(self.sample_spc_bndry)//2):
            self.scaled_sample_spc_bndry.append(-1)
            self.scaled_sample_spc_bndry.append(1)
            
        # Full factorial test points are generated
        self.full_fac = []
        self.compiled_full_fac = []
        for j in range(0, int(num_of_var)):

            for i in range(0,21 ** int(num_of_var)):
                # Full factorial (all possible points for test)
                # Notice that each variable assumed to have 21 points in 
                # a given range.
                self.full_fac.append(
                    (round(float(self.scaled_sample_spc_bndry[j * 2])
                    + ((float(self.scaled_sample_spc_bndry[2*j + 1]) 
                    - float(self.scaled_sample_spc_bndry[2 * j])) / 20) 
                    * ((i // (21**(int(num_of_var) - (j + 1)))) % 21), 2)))

        # Creates a list containing 5 lists, each of 8 items, all set to 0
        self.compiled_full_fac = [[0 for x in range(int(num_of_var))] 
                   for y in range(21 ** int(num_of_var))]

        # Let's turn the full factorial into list inside list structure. By 
        # this way it will be easier to reach test points for a defined step.
        for i in range(0, (21**int(num_of_var)) * int(num_of_var)):
            self.compiled_full_fac[
                i // int(num_of_var)][(i) % int(num_of_var)] \
                = self.full_fac[(i % int(num_of_var)) 
                                * (21 ** int(num_of_var)) 
                                + (i // int(num_of_var))]

        # There are several approaches (e.g. row exchange etc.) to reach 
        # d-optimality criterion but in my case I use reverse engineering to 
        # to determine what kind of patterns does professional programs 
        # produce to fulfill d-optimality criterion. For example if we take 3D 
        # sample space (i.e 3 test variables) then vertice points (i.e. points
        # which have either max or min of each variable) will be around 10 
        # percent, edge points will be around 40 percent and so on.
        #
        # For this let's determine the geometrical properties of test points.
        # This requires us to check how many max or min does each test point 
        # has.
        get_pnt_property = []
        for i in range(0, int(num_of_var) + 1):
            get_pnt_property.append([])
        
        for i in range(0, 21 ** int(num_of_var)):
            counter = 0
            for j in range(0, int(num_of_var)):
                if (self.compiled_full_fac[i][j] == -1 
                    or self.compiled_full_fac[i][j] == 1):
                    counter += 1
            get_pnt_property[counter].append(i + 1)
   

        # Let's determine requested point number for each category (i.e.
        # vertices, edges, faces etc.) For this let's start with 
        num_of_vertice = []  # Only 4 variables are max or min
        num_of_edge = []  # Only 3 variables are max or min
        num_of_face = []  # Only 2 variables are max or min
        num_of_volume = []  # Only 1 variable is max or min
        num_of_pnt_in_mid = []  # None of the variables are max or min          
        num_of_steps = int(num_of_steps)
        
        # Let's determine the number of points per each iteration in accordance
        # with geometrical category (vertice, edge and so on). Here the 
        # percentages are derived by reverse engineering.
        for i in range(0, num_of_iter): 
            verticeRand = random.randint(3,14)
            rem_steps = num_of_steps
            req_vertice_pnt_per_iter = round((verticeRand*num_of_steps) 
                                             / 100)
        
            if req_vertice_pnt_per_iter >= rem_steps:
                req_vertice_pnt_per_iter = rem_steps
                rem_steps = 0
            rem_steps = rem_steps-req_vertice_pnt_per_iter
            
            req_edge_pnt_per_iter = round(random.randint(36,50)*num_of_steps
                                          / 100)
            if req_edge_pnt_per_iter >= rem_steps:
                req_edge_pnt_per_iter = rem_steps
           
            rem_steps = rem_steps-req_edge_pnt_per_iter
            
            req_vol_pnt_per_iter = round(random.randint(8,16)*num_of_steps 
                                         / 100)
            if req_vol_pnt_per_iter >= rem_steps:
                req_vol_pnt_per_iter = rem_steps
           
            rem_steps = rem_steps-req_vol_pnt_per_iter      
            
            req_face_pnt_per_iter = round(random.randint(18,50)*num_of_steps
                                          / 100)
            if req_face_pnt_per_iter >= rem_steps:
                req_face_pnt_per_iter = rem_steps
           
            rem_steps = rem_steps - req_face_pnt_per_iter   

            req_pnt_in_mid_per_iter = round(random.randint(0,6)*num_of_steps 
                                            / 100)
            if req_pnt_in_mid_per_iter >= rem_steps:
                req_pnt_in_mid_per_iter = rem_steps
           
            rem_steps = rem_steps - req_pnt_in_mid_per_iter
            while rem_steps > 0:                
                if rem_steps>0:
                    req_vertice_pnt_per_iter += 1
                    rem_steps -= 1
                    
                if req_vertice_pnt_per_iter>round((num_of_steps*14)/100):
                    req_vertice_pnt_per_iter -= 1
                    rem_steps += 1 
                    
                if rem_steps>0:                    
                    req_edge_pnt_per_iter += 1
                    rem_steps -= 1
                    
                if req_edge_pnt_per_iter>round((num_of_steps*50)/100):
                    req_edge_pnt_per_iter -= 1                    
                    rem_steps += 1
                    
                if rem_steps>0:                    
                    req_face_pnt_per_iter += 1
                    rem_steps -= 1             
                
                if req_face_pnt_per_iter>round((num_of_steps*50)/100):
                    req_face_pnt_per_iter -= 1                    
                    rem_steps += 1
                
                if rem_steps>0:                    
                    req_vol_pnt_per_iter += 1
                    rem_steps -= 1
                
                if req_vol_pnt_per_iter>round((num_of_steps*16)/100):
                    req_vol_pnt_per_iter -= 1
                    rem_steps += 1
                
                if rem_steps>0:                    
                    req_pnt_in_mid_per_iter += 1
                    rem_steps -= 1
                
                if req_pnt_in_mid_per_iter>round((num_of_steps*6)/100):
                    req_pnt_in_mid_per_iter -= 1            
                    rem_steps += 1             

            num_of_vertice.append(req_vertice_pnt_per_iter)
            num_of_edge.append(req_edge_pnt_per_iter)
            num_of_face.append(req_face_pnt_per_iter)
            num_of_volume.append(req_vol_pnt_per_iter)
            num_of_pnt_in_mid.append(req_pnt_in_mid_per_iter)
        
        # Now it's time to generate information matrix. Our assumption is
        # 2. Order Taylor Series which is based upon the effect of the 
        # variables and their powers to each other.
        if sel_model == "2nd Order Taylor Series":
            selected_test_pnts = []
            for j in range(0,len(get_pnt_property)):
                selected_test_pnts.append([])
                
            # Randomly select test points from each category per iteration
            for i in range(0,num_of_iter):
                selected_test_pnts[4].append(
                    random.sample(range(0, len(get_pnt_property[4])),
                                  num_of_vertice[i]))
                selected_test_pnts[3].append(
                    random.sample(range(0, len(get_pnt_property[3])),
                                  num_of_edge[i]))
                selected_test_pnts[2].append(
                    random.sample(range(0, len(get_pnt_property[2])),
                                  num_of_face[i]))
                selected_test_pnts[1].append(
                    random.sample(range(0, len(get_pnt_property[1])),
                                  num_of_volume[i]))
                selected_test_pnts[0].append(
                    random.sample(range(0, len(get_pnt_property[0])),
                                  num_of_pnt_in_mid[i]))

            # Rearrange the list in order it to has list inside list structure.
            compiled_test_pnts = []            
            for k in range(0, len(get_pnt_property)):
                for i in range(0, num_of_iter):  #iterasyon sayısı
                    compiled_test_pnts.append([])
                    for j in range(0, len(selected_test_pnts[k][i])):
                        compiled_test_pnts[i].append(get_pnt_property[k][selected_test_pnts[k][i][j]])
                        
            final_test_pnts = []
            
            # Selected test points are rematched with full factorial test points.            
            for i in range(0, num_of_iter):
                final_test_pnts.append([])
                for j in range(0,len(compiled_test_pnts[i])):
                    final_test_pnts[i].append(
                        self.compiled_full_fac[compiled_test_pnts[i][j] - 1])
            print("final ", final_test_pnts)
            # Information matrix is generated from selected test points in 
            # accordance with model (2. Order Taylor Series).
            model_info_matrix = []
            for i in range(0, num_of_iter):
                model_info_matrix.append([])
                for j in range(0, len(final_test_pnts[i])):
                    model_info_matrix[i].append([])
                    for k in range(0, int(num_of_var)):
                        if k <= 0:
                            model_info_matrix[i][j].append(1)
                            for m in range(0, int(num_of_var)):                            
                                model_info_matrix[i][j].append(
                                    final_test_pnts[i][j][m])
                        for n in range(0, int(num_of_var) - k):
                            model_info_matrix[i][j].append(
                                round(final_test_pnts[i][j][k] 
                                      * final_test_pnts[i][j][k + n], 3))

            # Let X is information matrix. In that case we must find X' 
            # and try to maximize the determinant of X'X. Here iteration 
            # number is one factor which makes it converge more on to global 
            # optima.

            trnsposed_info_matrix = []
            trnsposed_dot_info_matrix = []
            self.det_of_trnsposed_dot_info = []
            # For iteration number, do the maximization of determinant of X'X.
            for i in range(0,num_of_iter):
                trnsposed_info_matrix.append([])
                trnsposed_dot_info_matrix.append([])
                # Transpose information matrix to find X'
                trnsposed_info_matrix[i] = np.transpose(model_info_matrix[i])
                # Evaluate X'X
                trnsposed_dot_info_matrix[i] = np.dot(trnsposed_info_matrix[i], 
                                                      model_info_matrix[i])
                # Evaluate determinant of X'X (Transposed info matrix dot 
                # matrix info)
                value_of_det = np.linalg.det(trnsposed_dot_info_matrix[i])
                self.det_of_trnsposed_dot_info.append(i)
                self.det_of_trnsposed_dot_info.append(value_of_det)
                print(i,". iteration determinant is",value_of_det)

            # Highest value of determinant of X'X is selected.
            max_value = max(self.det_of_trnsposed_dot_info)
            idx_of_max = self.det_of_trnsposed_dot_info.index(max_value)
            corr_idx_of_max = round(((idx_of_max - 1) / 2) + 1)
            print(idx_of_max,"önce ve sonrası", corr_idx_of_max)

            rescld_final_test_points = []
            for j in range(0,int(num_of_steps)):
                rescld_final_test_points.append([])
                    
            # Selected points from maximization of det of X'X are rescaled to
            # their original values.
            for j in range(0,int(num_of_steps)):
                for k in range(0,int(num_of_var)):
                    # Rescale the points to the actual values
                    rescld_final_test_points[j].append(
                        round((final_test_pnts[corr_idx_of_max - 1][j][k] 
                        * (float(self.sample_spc_bndry[2*k + 1]) 
                        - float(self.sample_spc_bndry[2 * k])) 
                        + float(self.sample_spc_bndry[2*k + 1]) 
                        + float(self.sample_spc_bndry[2*k])) / 2, 1))

        # Now let's export the final test points to csv.
        with open('test_points.csv', mode='w', newline='') as test_points:
            test_points_to_csv = csv.writer(
                test_points, delimiter=',', quotechar='"')#, quoting=csv.QUOTE_MINIMAL)
            test_points_to_csv.writerows(rescld_final_test_points)

        # Let's write full factorial of test points to csv                
        with open('all_avail_pnts.csv', mode='w',newline='') as all_avail_pnts:
            full_fac_to_csv = csv.writer(all_avail_pnts, 
                                         delimiter=',', quotechar='"')
            full_fac_to_csv.writerows(self.compiled_full_fac)
            
        return self.doe_variables,  \
                self.det_of_trnsposed_dot_info, rescld_final_test_points
