# https://www.youtube.com/watch?v=LTmTDht1PQ8
import sqlite3,sys, os
import streamlit as st
import google.generativeai as genai
sys.path.append(os.path.abspath(os.path.join('../..', 'secret')))
from secret_info import google_genai_api

GOGGLE_API_KEY = google_genai_api
genai.configure(api_key = GOGGLE_API_KEY)
model=genai.GenerativeModel('gemini-1.5-pro-latest')
## Define Your Prompt
# The original prompt had a text description of the database created with sql_creator. THe below is the 
# schema extracted from chinook database using sqlite3 db.get_table_info()
prompt=['''The following is the structure of the data base:       
CREATE TABLE albums (
	"AlbumId" INTEGER NOT NULL, 
	"Title" NVARCHAR(160) NOT NULL, 
	"ArtistId" INTEGER NOT NULL, 
	PRIMARY KEY ("AlbumId"), 
	FOREIGN KEY("ArtistId") REFERENCES artists ("ArtistId")
)
/*
3 rows from albums table:
AlbumId	Title	ArtistId
1	For Those About To Rock We Salute You	1
2	Balls to the Wall	2
3	Restless and Wild	2
*/
CREATE TABLE artists (
	"ArtistId" INTEGER NOT NULL, 
	"Name" NVARCHAR(120), 
	PRIMARY KEY ("ArtistId")
)
/*
3 rows from artists table:
ArtistId	Name
1	AC/DC
2	Accept
3	Aerosmith
*/
CREATE TABLE customers (
	"CustomerId" INTEGER NOT NULL, 
	"FirstName" NVARCHAR(40) NOT NULL, 
	"LastName" NVARCHAR(20) NOT NULL, 
	"Company" NVARCHAR(80), 
	"Address" NVARCHAR(70), 
	"City" NVARCHAR(40), 
	"State" NVARCHAR(40), 
	"Country" NVARCHAR(40), 
	"PostalCode" NVARCHAR(10), 
	"Phone" NVARCHAR(24), 
	"Fax" NVARCHAR(24), 
	"Email" NVARCHAR(60) NOT NULL, 
	"SupportRepId" INTEGER, 
	PRIMARY KEY ("CustomerId"), 
	FOREIGN KEY("SupportRepId") REFERENCES employees ("EmployeeId")
)
/*
3 rows from customers table:
CustomerId	FirstName	LastName	Company	Address	City	State	Country	PostalCode	Phone	Fax	Email	SupportRepId
1	Luís	Gonçalves	Embraer - Empresa Brasileira de Aeronáutica S.A.	Av. Brigadeiro Faria Lima, 2170	São José dos Campos	SP	Brazil	12227-000	+55 (12) 3923-5555	+55 (12) 3923-5566	luisg@embraer.com.br	3
2	Leonie	Köhler	None	Theodor-Heuss-Straße 34	Stuttgart	None	Germany	70174	+49 0711 2842222	None	leonekohler@surfeu.de	5
3	François	Tremblay	None	1498 rue Bélanger	Montréal	QC	Canada	H2G 1A7	+1 (514) 721-4711	None	ftremblay@gmail.com	3
*/
CREATE TABLE employees (
	"EmployeeId" INTEGER NOT NULL, 
	"LastName" NVARCHAR(20) NOT NULL, 
	"FirstName" NVARCHAR(20) NOT NULL, 
	"Title" NVARCHAR(30), 
	"ReportsTo" INTEGER, 
	"BirthDate" DATETIME, 
	"HireDate" DATETIME, 
	"Address" NVARCHAR(70), 
	"City" NVARCHAR(40), 
	"State" NVARCHAR(40), 
	"Country" NVARCHAR(40), 
	"PostalCode" NVARCHAR(10), 
	"Phone" NVARCHAR(24), 
	"Fax" NVARCHAR(24), 
	"Email" NVARCHAR(60), 
	PRIMARY KEY ("EmployeeId"), 
	FOREIGN KEY("ReportsTo") REFERENCES employees ("EmployeeId")
)
/*
3 rows from employees table:
EmployeeId	LastName	FirstName	Title	ReportsTo	BirthDate	HireDate	Address	City	State	Country	PostalCode	Phone	Fax	Email
1	Adams	Andrew	General Manager	None	1962-02-18 00:00:00	2002-08-14 00:00:00	11120 Jasper Ave NW	Edmonton	AB	Canada	T5K 2N1	+1 (780) 428-9482	+1 (780) 428-3457	andrew@chinookcorp.com
2	Edwards	Nancy	Sales Manager	1	1958-12-08 00:00:00	2002-05-01 00:00:00	825 8 Ave SW	Calgary	AB	Canada	T2P 2T3	+1 (403) 262-3443	+1 (403) 262-3322	nancy@chinookcorp.com
3	Peacock	Jane	Sales Support Agent	2	1973-08-29 00:00:00	2002-04-01 00:00:00	1111 6 Ave SW	Calgary	AB	Canada	T2P 5M5	+1 (403) 262-3443	+1 (403) 262-6712	jane@chinookcorp.com
*/
CREATE TABLE genres (
	"GenreId" INTEGER NOT NULL, 
	"Name" NVARCHAR(120), 
	PRIMARY KEY ("GenreId")
)
/*
3 rows from genres table:
GenreId	Name
1	Rock
2	Jazz
3	Metal
*/
CREATE TABLE invoice_items (
	"InvoiceLineId" INTEGER NOT NULL, 
	"InvoiceId" INTEGER NOT NULL, 
	"TrackId" INTEGER NOT NULL, 
	"UnitPrice" NUMERIC(10, 2) NOT NULL, 
	"Quantity" INTEGER NOT NULL, 
	PRIMARY KEY ("InvoiceLineId"), 
	FOREIGN KEY("TrackId") REFERENCES tracks ("TrackId"), 
	FOREIGN KEY("InvoiceId") REFERENCES invoices ("InvoiceId")
)
/*
3 rows from invoice_items table:
InvoiceLineId	InvoiceId	TrackId	UnitPrice	Quantity
1	1	2	0.99	1
2	1	4	0.99	1
3	2	6	0.99	1
*/
CREATE TABLE invoices (
	"InvoiceId" INTEGER NOT NULL, 
	"CustomerId" INTEGER NOT NULL, 
	"InvoiceDate" DATETIME NOT NULL, 
	"BillingAddress" NVARCHAR(70), 
	"BillingCity" NVARCHAR(40), 
	"BillingState" NVARCHAR(40), 
	"BillingCountry" NVARCHAR(40), 
	"BillingPostalCode" NVARCHAR(10), 
	"Total" NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY ("InvoiceId"), 
	FOREIGN KEY("CustomerId") REFERENCES customers ("CustomerId")
)
/*
3 rows from invoices table:
InvoiceId	CustomerId	InvoiceDate	BillingAddress	BillingCity	BillingState	BillingCountry	BillingPostalCode	Total
1	2	2009-01-01 00:00:00	Theodor-Heuss-Straße 34	Stuttgart	None	Germany	70174	1.98
2	4	2009-01-02 00:00:00	Ullevålsveien 14	Oslo	None	Norway	0171	3.96
3	8	2009-01-03 00:00:00	Grétrystraat 63	Brussels	None	Belgium	1000	5.94
*/
CREATE TABLE media_types (
	"MediaTypeId" INTEGER NOT NULL, 
	"Name" NVARCHAR(120), 
	PRIMARY KEY ("MediaTypeId")
)
/*
3 rows from media_types table:
MediaTypeId	Name
1	MPEG audio file
2	Protected AAC audio file
3	Protected MPEG-4 video file
*/
CREATE TABLE playlist_track (
	"PlaylistId" INTEGER NOT NULL, 
	"TrackId" INTEGER NOT NULL, 
	PRIMARY KEY ("PlaylistId", "TrackId"), 
	FOREIGN KEY("TrackId") REFERENCES tracks ("TrackId"), 
	FOREIGN KEY("PlaylistId") REFERENCES playlists ("PlaylistId")
)
/*
3 rows from playlist_track table:
PlaylistId	TrackId
1	3402
1	3389
1	3390
*/
CREATE TABLE playlists (
	"PlaylistId" INTEGER NOT NULL, 
	"Name" NVARCHAR(120), 
	PRIMARY KEY ("PlaylistId")
)
/*
3 rows from playlists table:
PlaylistId	Name
1	Music
2	Movies
3	TV Shows
*/
CREATE TABLE tracks (
	"TrackId" INTEGER NOT NULL, 
	"Name" NVARCHAR(200) NOT NULL, 
	"AlbumId" INTEGER, 
	"MediaTypeId" INTEGER NOT NULL, 
	"GenreId" INTEGER, 
	"Composer" NVARCHAR(220), 
	"Milliseconds" INTEGER NOT NULL, 
	"Bytes" INTEGER, 
	"UnitPrice" NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY ("TrackId"), 
	FOREIGN KEY("MediaTypeId") REFERENCES media_types ("MediaTypeId"), 
	FOREIGN KEY("GenreId") REFERENCES genres ("GenreId"), 
	FOREIGN KEY("AlbumId") REFERENCES albums ("AlbumId")
)
/*
3 rows from tracks table:
TrackId	Name	AlbumId	MediaTypeId	GenreId	Composer	Milliseconds	Bytes	UnitPrice
1	For Those About To Rock (We Salute You)	1	1	1	Angus Young, Malcolm Young, Brian Johnson	343719	11170334	0.99
2	Balls to the Wall	2	2	1	None	342562	5510424	0.99
3	Fast As a Shark	3	2	1	F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman	230619	3990994	0.99
*/
The SQL code should not have ``` in beginning or end and sql word in output
'''
]

def get_gemini_response(model, question):
		response = model.generate_content(question)
		return response.text

def read_sql_query(sql,db, prnt = False):
		conn=sqlite3.connect(db)
		cur=conn.cursor()
		cur.execute(sql)
		rows=cur.fetchall()
		conn.commit()
		conn.close()
		if prnt == True:
			print("This is the query:\n" , sql)
			for row in rows:
				print(row)
		return rows

def main():
    dtb = "chinook.db"
    st.set_page_config(page_title = 'SQL QUERY GENEATOR', page_icon = ':robot:')
    st.markdown(
        f'''
        <div style = 'text-align: center;'>
            <h1> SQL Query Generator </h1>
        </div>
        ''',
        unsafe_allow_html = True,
    )
    st.header(f"Gemini App To Retrieve Data from: \n\t{dtb}")
    text_input = st.text_area('Enter your question here: ')
    submit = st.button("Get your answer")
    if submit:
        with st.spinner("Generating SQL QUERY..."):
            template =  """
                        '''
                        {text_input}
                        '''
                        I just want a sql query 
                        """
            formatted_template = template.format(text_input = text_input)
            # response = model.generate_content(formatted_template)[prompt[0],question]
            sql_query = get_gemini_response(model, [prompt[0],formatted_template])
            sql_query = sql_query.strip().lstrip("```sql").rstrip("```")
            # expected_output = """
            #                   What would be the expected response for this SQL query snipper
            #                   '''
            #                   {sql_query}
            #                   '''
            #                   Provide sample tabular response with no explanation 
            #                   """
            # expected_output_formated = expected_output.format(sql_query = sql_query)  
            eoutput=read_sql_query(sql_query,dtb, False)
            # eoutput = get_gemini_response(model, expected_output_formated)
            explanation =   """
                            Explain this SQL query result
                            '''
                            {sql_query}
                            '''
                            Please provide with simples of explanations
                            """
            explanation_formated = explanation.format(sql_query = sql_query)
            exoutput = get_gemini_response(model, explanation_formated)
            response_final =   """
                            Explain the results based on the question
                            '''
                            {text_input}
                            {eoutput}
                            '''
                            Please provide with simples of explanations
                            """
            response_final_formated = response_final.format(text_input = text_input, eoutput = eoutput)
            explanation_response = get_gemini_response(model, response_final_formated)
            with st.container():
                st.success("THE ANSWER IS:") 
                st.markdown(explanation_response)  
                st.success("This is the query: ") 
                st.code(sql_query, language = 'sql')    
                st.success("The output of the query is: ") 
                st.markdown(eoutput)       
                st.success("Take a look at the explanation for the query:") 
                st.markdown(exoutput)   
main()