<?php
/*
  PHP command-line XML schema validation tester.

  Usage: php schema_filename.xsd xml_filename.xml
  
  This script attempts to validate an XML test file against an XML schema file.
  Any errors detected in the schema or test file are printed to the console 
  at the end of the run.
*/

error_reporting(0); // Rely on custom error reporting

if (count ($argv) != 3) {
  die ("Usage: php " . __FILE__ . " schema_filename.xsd xml_filename.xml\n");
}

$schema_file = $argv[1];
$test_xml = $argv[2];

// Enable user error handling
libxml_use_internal_errors(true);

$d = new DomDocument();
if (@$d->loadXML(file_get_contents ($test_xml)) === FALSE) {
  die ("Unable to load XML\n");
}

if (!$d->schemaValidate($schema_file)) {
  libxml_display_errors();
	die ("\nErrors found\n");
}
      
print "\nValidation success\n";


// https://www.php.net/manual/en/domdocument.schemavalidate.php
function libxml_display_error($error)
{
    global $argv;

    $return = "";
    switch ($error->level) {
        case LIBXML_ERR_WARNING:
            $return .= "Warning $error->code: ";
            break;
        case LIBXML_ERR_ERROR:
            $return .= "Error $error->code: ";
            break;
        case LIBXML_ERR_FATAL:
            $return .= "Fatal Error $error->code: ";
            break;
    }
    $return .= trim($error->message);
    // $error->file is reliable for declaring the schema filename but not so much the test XML filename
    $return .=  (stripos($error->file, '.xsd') !== false || stripos($error->file, '.xml') !== false) ? " in $error->file" : " in $argv[2]";
    $return .= " on line $error->line\n";

    return $return;
}

function libxml_display_errors() {
    $errors = libxml_get_errors();
    foreach ($errors as $error) {
        print libxml_display_error($error);
    }
    libxml_clear_errors();
}

