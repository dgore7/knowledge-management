
## Functionality Overview
1.  Tag content with metadata: i.e. Allowing the input of data that classifies content (e.g. keywords) so that it can be searched for and retrieved.
    * Storing tags/keywords in the database
2. Make it easy to edit content
    * Allow for notes and comments within repositories
3. Version control: Tracking changes to pages and, if necessary, allowing previous versions to be accessed
    * Allow editors to have access to previous versions of the content
4. Searchability
    * Allow to search for repositories and content within repositories
    * Search by metadata (file extensions, date created/modified)
5. Allow for collaborative work on content
    * Create directories of shared content
    * Attach access to certain repositories
    * Allow for shared, public, and private repositories
6. Integrated document management systems
    * Ability to upload and download files from the system
7. Ease of use
    * Simple and straightforward user interface (GUI) 
8. A secure system
    * Authentication and encryption of user information
    * File and content encryption 
    * System that self manages certificates
    
## Technical Architecture

* Server 
    * models
        * data modeling
        * database access and queries
    * controllers
        * provides an interface for interacting with the data layer which mimics the options of our protocol
    * server will maintain document access level
    *  facilitate versioning for documents
* Client
    * request documents
    * search documents/notes based on tags

## Wireframes of End Goal (Subject to Change):

## TODO
* File Version Control
* Search caching
* Tag sorting/completion
   * based on usage/frequency


