import streamlit as st,pandas as pd,os, math

#user input

def size_input():
	original_title = '<p style="font-family:Sans serif; color:Magenta; font-size: 30px;"><b>Collection Amount</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col1, col2, col3 = st.columns(3)
	with col1:
		collectionsize = st.number_input("Enter Size of Collection (in km)",min_value=5,max_value=200,step=5)
	original_title = '<p style="font-family:Sans serif; color:Magenta; font-size: 30px;"><b>Storage Filling Type</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	fillperct = st.radio("Select filling percentage",('Fixed rack (35%)','Mobile rack (80%)','Custom Filling Percentage'))
	if(fillperct == 'Custom Filling Percentage'):
		colp, colq, colr = st.columns(3)
		with colp:
			fillperctvalue = st.number_input("Enter Filling Percentage",min_value=10,max_value=80,step=5)
	else:
		fillperctvalue = int(fillperct[-4:-2])

	original_title = '<p style="font-family:Sans serif; color:Magenta; font-size: 30px;"><b>Repository Dimesnion</b></p>'
	st.markdown(original_title, unsafe_allow_html=True)
	col5, col6, col7 = st.columns(3)
	with col5:
		repo_length = st.number_input("Enter Length of Repository (in m)",min_value=5,max_value=100,value=15,step=5,key='length')
	with col6:
		repo_width = st.number_input("Enter Width of Repository (in m)",min_value=5,max_value=100,value=10,step=5,key='width')
	with col7:
		repo_floorheight = st.number_input("Enter Height of each Floor (in m)",min_value=3.5,max_value=6.0,value=4.0,step=0.5,key='height',format="%.1f")

	collection_volume = collectionsize*1000*0.4*0.26
	building_volume = (collection_volume*100)/fillperctvalue
	totalinitialheight = (building_volume/(repo_width*repo_length))
	number_of_floors = math.ceil(totalinitialheight/repo_floorheight)

	if(number_of_floors > 3):
		st.error("Calculated number of floors for the archive is higher than 3. Please change length/width or filling type of repository to make the budiling of max 3 floors", icon="⚠️")

# 	valuelist = [collectionsize,fillperctvalue,repo_length,repo_width,repo_floorheight, number_of_floors]
# 	columnlist = ['Collection Size (km)', 'Filling Percentage (%)', 'Repository Length (m)', 'Repository Width (m)', 'Repository Floor Height (m)', 'Number of Floors']


# 	#Current working directory
# 	cwd = os.getcwd()
# 	#set path to subdirectory and inputfilename
# 	inputfilesnamewithpath = cwd+'\\Inputfiles\\RepositoryUserInputs.csv'


# 	#Write the inputs to a csv file
# 	inputdf = pd.DataFrame([valuelist], columns = columnlist)
# 	inputdf.to_csv(inputfilesnamewithpath, index=False)
	

