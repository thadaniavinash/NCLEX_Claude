// Pull the latest question bank from NCLEX_Claude's own Supabase project into cases-data.js.
// Same as: node tools/supabase.js download
process.argv[2] = 'download';
require('./tools/supabase.js');
