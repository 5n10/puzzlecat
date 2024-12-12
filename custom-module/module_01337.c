/**
 * Author......: See docs/credits.txt
 * License.....: MIT
 */

#include "common.h"
#include "types.h"
#include "modules.h"
#include "bitops.h"
#include "convert.h"
#include "shared.h"
#include "memory.h"

#include "emu_inc_hash_base58.h"

static const u32   ATTACK_EXEC       = ATTACK_EXEC_OUTSIDE_KERNEL;
static const u32   DGST_POS0         = 0;
static const u32   DGST_POS1         = 1;
static const u32   DGST_POS2         = 2;
static const u32   DGST_POS3         = 3;
static const u32   DGST_SIZE         = DGST_SIZE_4_5;
static const u32   HASH_CATEGORY     = HASH_CATEGORY_CRYPTOCURRENCY_WALLET;
static const char *HASH_NAME         = "Brainwallet, Uncompressed";
static const u64   KERN_TYPE         = 1337;
static const u32   OPTI_TYPE         = OPTI_TYPE_NOT_SALTED;
static const u64   OPTS_TYPE         = OPTS_TYPE_PT_GENERATE_LE;
static const u32   SALT_TYPE         = SALT_TYPE_NONE;
static const char *ST_PASS           = "hashcat";
//static const char *ST_HASH           = "7f67c2c704bc1eac097fed3bf31963a8f817bfc3";
static const char *ST_HASH           = "1Ccf7nyWhoQGqX5T5xxzNJ77oUdruP2KRx";
static const char *BENCHMARK_MASK    = "ha?1?1?1?1?1";
static const char *BENCHMARK_CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
//static const u32   PUBKEY_MAXLEN     = 64; // our max is actually always 25 (21 + 4)
//static const u32   WIF_LEN           = 52;



u32         module_attack_exec       (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return ATTACK_EXEC;     }
u32         module_dgst_pos0         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return DGST_POS0;       }
u32         module_dgst_pos1         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return DGST_POS1;       }
u32         module_dgst_pos2         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return DGST_POS2;       }
u32         module_dgst_pos3         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return DGST_POS3;       }
u32         module_dgst_size         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return DGST_SIZE;       }
u32         module_hash_category     (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return HASH_CATEGORY;   }
const char *module_hash_name         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return HASH_NAME;       }
u64         module_kern_type         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return KERN_TYPE;       }
u32         module_opti_type         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return OPTI_TYPE;       }
u64         module_opts_type         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return OPTS_TYPE;       }
u32         module_salt_type         (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return SALT_TYPE;       }
const char *module_st_hash           (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return ST_HASH;         }
const char *module_st_pass           (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return ST_PASS;         }
const char *module_benchmark_mask    (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return BENCHMARK_MASK;  }
const char *module_benchmark_charset (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra) { return BENCHMARK_CHARSET;  }

typedef struct brainwallet_tmp
{
  u32 digest_buf[4];

} brainwallet_tmp_t;



u64 module_tmp_size (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra)
{
  const u64 tmp_size = (const u64) sizeof (brainwallet_tmp_t);

  return tmp_size;
}

void print_u32_array_as_chars(u32 *array, int size) {
    for (size_t i = 0; i < size; i++) {
        // Extract each byte from the 32-bit integer
        char c1 = (array[i] >> 24) & 0xFF;
        char c2 = (array[i] >> 16) & 0xFF;
        char c3 = (array[i] >> 8) & 0xFF;
        char c4 = array[i] & 0xFF;

        // Print each character
        printf("%c%c%c%c", c1, c2, c3, c4);
    }
    printf("\n"); // Print a newline at the end
}

void print_u32_array_as_hex(u32 *array, int size) {
    if (array == NULL || size <= 0) {
        printf("Invalid array or size.\n");
        return;
    }

    for (int i = 0; i < size; i++) {
        u8 byte1 = (array[i] >> 24) & 0xFF;
        u8 byte2 = (array[i] >> 16) & 0xFF;
        u8 byte3 = (array[i] >> 8) & 0xFF;
        u8 byte4 = array[i] & 0xFF;

        printf("%02X %02X %02X %02X ", byte1, byte2, byte3, byte4);
    }
    printf("\n");
}


u32 module_pw_max (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra)
{
  return 64;
}

u32 module_pw_min (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const user_options_t *user_options, MAYBE_UNUSED const user_options_extra_t *user_options_extra)
{
  return 1;
}

int module_hash_decode (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED void *digest_buf, MAYBE_UNUSED salt_t *salt, MAYBE_UNUSED void *esalt_buf, MAYBE_UNUSED void *hook_salt_buf, MAYBE_UNUSED hashinfo_t *hash_info, const char *line_buf, MAYBE_UNUSED const int line_len)
{
  static const u32   PUBKEY_MAXLEN     = 64; // our max is actually always 25 (21 + 4)
  u8 *digest = (u8 *) digest_buf;

  u8 pubkey[PUBKEY_MAXLEN];

  hc_token_t token;

  token.token_cnt = 1;

  token.len_min[0] = 26;
  token.len_max[0] = 34;
  token.attr[0]    = TOKEN_ATTR_VERIFY_LENGTH
                   | TOKEN_ATTR_VERIFY_BASE58;

  const int rc_tokenizer = input_tokenizer ((const u8 *) line_buf, line_len, &token);

  if (rc_tokenizer != PARSER_OK) return (rc_tokenizer);

  u32 pubkey_len = PUBKEY_MAXLEN;

  bool res = b58dec (pubkey, &pubkey_len, (u8 *) line_buf, line_len);

  if (res == false) return (PARSER_HASH_LENGTH);

  // for now we support only P2PKH addresses

  if (pubkey_len != 25) return (PARSER_HASH_LENGTH); // most likely wrong Bitcoin address type

  u32 l = PUBKEY_MAXLEN - pubkey_len;

  if (pubkey[l] != 0) return (PARSER_HASH_VALUE); // wrong Bitcoin address type

  // check if pubkey has correct sha256 sum included

  u32 npubkey[16] = { 0 };

  u8 *npubkey_ptr = (u8 *) npubkey;

  for (u32 i = 0, j = PUBKEY_MAXLEN - pubkey_len; i < pubkey_len; i++, j++)
  {
    npubkey_ptr[i] = pubkey[j];
  }

  // if (b58check   (npubkey_ptr, pubkey_len) == false) return (PARSER_HASH_ENCODING);
  // if (b58check64 (npubkey,     pubkey_len) == false) return (PARSER_HASH_ENCODING);

  if (b58check_25 (npubkey) == false) return (PARSER_HASH_ENCODING);


  for (u32 i = 0; i < 20; i++) // DGST_SIZE
  {
    digest[i] = pubkey[PUBKEY_MAXLEN - pubkey_len + i + 1];
  }


      printf("Digest: %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u %u\n", 
       digest[0], digest[1], digest[2], digest[3], digest[4], 
       digest[5], digest[6], digest[7], digest[8], digest[9], 
       digest[10], digest[11], digest[12], digest[13], digest[14], 
       digest[15], digest[16], digest[17], digest[18], digest[19]);




  return (PARSER_OK); 

  
  /*
  //RIPMD implementation below
   u32 *digest = (u32 *) digest_buf;

  hc_token_t token;

  token.token_cnt  = 1;

  token.len_min[0] = 40;
  token.len_max[0] = 40;
  token.attr[0]    = TOKEN_ATTR_VERIFY_LENGTH
                   | TOKEN_ATTR_VERIFY_HEX;

  const int rc_tokenizer = input_tokenizer ((const u8 *) line_buf, line_len, &token);

  if (rc_tokenizer != PARSER_OK) return (rc_tokenizer);

  const u8 *hash_pos = token.buf[0];

  digest[0] = hex_to_u32 (hash_pos +  0);
  digest[1] = hex_to_u32 (hash_pos +  8);
  digest[2] = hex_to_u32 (hash_pos + 16);
  digest[3] = hex_to_u32 (hash_pos + 24);
  digest[4] = hex_to_u32 (hash_pos + 32);




      printf("Digest-160: %u %u %u %u %u\n", 
       digest[0], digest[1], digest[2], digest[3], digest[4]);


  return (PARSER_OK);*/

}


int module_hash_encode (MAYBE_UNUSED const hashconfig_t *hashconfig, MAYBE_UNUSED const void *digest_buf, MAYBE_UNUSED const salt_t *salt, MAYBE_UNUSED const void *esalt_buf, MAYBE_UNUSED const void *hook_salt_buf, MAYBE_UNUSED const hashinfo_t *hash_info, char *line_buf, MAYBE_UNUSED const int line_size)
{
  printf("\n\n encode \n\n");
  u8 *digest = (u8 *) digest_buf;

  u8 buf[64] = { 0 };

  u32 len = 64;

  b58check_enc (buf, &len, 0, digest, 20);

  return snprintf (line_buf, line_size, "%s", buf);
}


void module_init (module_ctx_t *module_ctx)
{
  module_ctx->module_context_size             = MODULE_CONTEXT_SIZE_CURRENT;
  module_ctx->module_interface_version        = MODULE_INTERFACE_VERSION_CURRENT;

  module_ctx->module_attack_exec              = module_attack_exec;
  module_ctx->module_benchmark_esalt          = MODULE_DEFAULT;
  module_ctx->module_benchmark_hook_salt      = MODULE_DEFAULT;
  module_ctx->module_benchmark_mask           = MODULE_DEFAULT;
  module_ctx->module_benchmark_charset        = MODULE_DEFAULT;
  module_ctx->module_benchmark_salt           = MODULE_DEFAULT;
  module_ctx->module_build_plain_postprocess  = MODULE_DEFAULT;
  module_ctx->module_deep_comp_kernel         = MODULE_DEFAULT;
  module_ctx->module_deprecated_notice        = MODULE_DEFAULT;
  module_ctx->module_dgst_pos0                = module_dgst_pos0;
  module_ctx->module_dgst_pos1                = module_dgst_pos1;
  module_ctx->module_dgst_pos2                = module_dgst_pos2;
  module_ctx->module_dgst_pos3                = module_dgst_pos3;
  module_ctx->module_dgst_size                = module_dgst_size;
  module_ctx->module_dictstat_disable         = MODULE_DEFAULT;
  module_ctx->module_esalt_size               = MODULE_DEFAULT;
  module_ctx->module_extra_buffer_size        = MODULE_DEFAULT;
  module_ctx->module_extra_tmp_size           = MODULE_DEFAULT;
  module_ctx->module_extra_tuningdb_block     = MODULE_DEFAULT;
  module_ctx->module_forced_outfile_format    = MODULE_DEFAULT;
  module_ctx->module_hash_binary_count        = MODULE_DEFAULT;
  module_ctx->module_hash_binary_parse        = MODULE_DEFAULT;
  module_ctx->module_hash_binary_save         = MODULE_DEFAULT;
  module_ctx->module_hash_decode_postprocess  = MODULE_DEFAULT;
  module_ctx->module_hash_decode_potfile      = MODULE_DEFAULT;
  module_ctx->module_hash_decode_zero_hash    = MODULE_DEFAULT;
  module_ctx->module_hash_decode              = module_hash_decode;
  module_ctx->module_hash_encode_status       = MODULE_DEFAULT;
  module_ctx->module_hash_encode_potfile      = MODULE_DEFAULT;
  module_ctx->module_hash_encode              = module_hash_encode;
  module_ctx->module_hash_init_selftest       = MODULE_DEFAULT;
  module_ctx->module_hash_mode                = MODULE_DEFAULT;
  module_ctx->module_hash_category            = module_hash_category;
  module_ctx->module_hash_name                = module_hash_name;
  module_ctx->module_hashes_count_min         = MODULE_DEFAULT;
  module_ctx->module_hashes_count_max         = MODULE_DEFAULT;
  module_ctx->module_hlfmt_disable            = MODULE_DEFAULT;
  module_ctx->module_hook_extra_param_size    = MODULE_DEFAULT;
  module_ctx->module_hook_extra_param_init    = MODULE_DEFAULT;
  module_ctx->module_hook_extra_param_term    = MODULE_DEFAULT;
  module_ctx->module_hook12                   = MODULE_DEFAULT;
  module_ctx->module_hook23                   = MODULE_DEFAULT;
  module_ctx->module_hook_salt_size           = MODULE_DEFAULT;
  module_ctx->module_hook_size                = MODULE_DEFAULT;
  module_ctx->module_jit_build_options        = MODULE_DEFAULT;
  module_ctx->module_jit_cache_disable        = MODULE_DEFAULT;
  module_ctx->module_kernel_accel_max         = MODULE_DEFAULT;
  module_ctx->module_kernel_accel_min         = MODULE_DEFAULT;
  module_ctx->module_kernel_loops_max         = MODULE_DEFAULT;
  module_ctx->module_kernel_loops_min         = MODULE_DEFAULT;
  module_ctx->module_kernel_threads_max       = MODULE_DEFAULT;
  module_ctx->module_kernel_threads_min       = MODULE_DEFAULT;
  module_ctx->module_kern_type                = module_kern_type;
  module_ctx->module_kern_type_dynamic        = MODULE_DEFAULT;
  module_ctx->module_opti_type                = module_opti_type;
  module_ctx->module_opts_type                = module_opts_type;
  module_ctx->module_outfile_check_disable    = MODULE_DEFAULT;
  module_ctx->module_outfile_check_nocomp     = MODULE_DEFAULT;
  module_ctx->module_potfile_custom_check     = MODULE_DEFAULT;
  module_ctx->module_potfile_disable          = MODULE_DEFAULT;
  module_ctx->module_potfile_keep_all_hashes  = MODULE_DEFAULT;
  module_ctx->module_pwdump_column            = MODULE_DEFAULT;
  module_ctx->module_pw_max                   = module_pw_max;
  module_ctx->module_pw_min                   = module_pw_min;
  module_ctx->module_salt_max                 = MODULE_DEFAULT;
  module_ctx->module_salt_min                 = MODULE_DEFAULT;
  module_ctx->module_salt_type                = module_salt_type;
  module_ctx->module_separator                = MODULE_DEFAULT;
  module_ctx->module_st_hash                  = module_st_hash;
  module_ctx->module_st_pass                  = module_st_pass;
  module_ctx->module_tmp_size                 = module_tmp_size;
  module_ctx->module_unstable_warning         = MODULE_DEFAULT;
  module_ctx->module_warmup_disable           = MODULE_DEFAULT;
}
