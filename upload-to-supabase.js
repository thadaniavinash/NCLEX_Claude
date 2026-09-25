// Upload cases-data.js to NCLEX_Claude's own Supabase project (never the original app's).
// Same as: node tools/supabase.js upload
process.argv[2] = 'upload';
require('./tools/supabase.js');
