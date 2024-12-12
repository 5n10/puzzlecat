/**
 * Author......: See docs/credits.txt
 * License.....: MIT
 */

//#define NEW_SIMD_CODE

#define SECP256K1_TMPS_TYPE PRIVATE_AS

#ifdef KERNEL_STATIC
#include M2S(INCLUDE_PATH/inc_vendor.h)
#include M2S(INCLUDE_PATH/inc_types.h)
#include M2S(INCLUDE_PATH/inc_platform.cl)
#include M2S(INCLUDE_PATH/inc_common.cl)
#include M2S(INCLUDE_PATH/inc_rp.h)
#include M2S(INCLUDE_PATH/inc_rp.cl)
#include M2S(INCLUDE_PATH/inc_scalar.cl)
#include M2S(INCLUDE_PATH/inc_hash_base58.cl)
#include M2S(INCLUDE_PATH/inc_hash_sha256.cl)
#include M2S(INCLUDE_PATH/inc_hash_ripemd160.cl)
#include M2S(INCLUDE_PATH/inc_ecc_secp256k1.cl)
#include M2S(INCLUDE_PATH/inc_hash_md5.cl)

#endif


#define COMPARE_S M2S(INCLUDE_PATH/inc_comp_single.cl)
#define COMPARE_M M2S(INCLUDE_PATH/inc_comp_multi.cl)

#ifndef NULL
#define NULL 0L
#endif


void print_u32_array_as_chars(u32 *array, int size) {
    for (size_t i = 0; i < size; i++) {
        // Extract each byte from the 32-bit integer
        char c4 = (array[i] >> 24) & 0xFF;
        char c3 = (array[i] >> 16) & 0xFF;
        char c2 = (array[i] >> 8) & 0xFF;
        char c1 = array[i] & 0xFF;

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
        u8 byte4 = (array[i] >> 24) & 0xFF;
        u8 byte3 = (array[i] >> 16) & 0xFF;
        u8 byte2 = (array[i] >> 8) & 0xFF;
        u8 byte1 = array[i] & 0xFF;

        printf("%02X %02X %02X %02X ", byte1, byte2, byte3, byte4);
    }
    printf("\n");
}

void printArrayAsChars(const u32 arr[], int size) {
    for (int i = 0; i < size; ++i) {
            printf("%c ", (char)arr[i]);
       
    }
    printf("\n");  // Newline at the end
}

void u32_to_char(const u32 value, char *chars)
{
  chars[0] = (value >> 24) & 0xFF;  // Extract the highest byte
  chars[1] = (value >> 16) & 0xFF;  // Extract the second-highest byte
  chars[2] = (value >> 8) & 0xFF;   // Extract the second-lowest byte
  chars[3] = value & 0xFF;          // Extract the lowest byte
}


/**
 * Author......: See docs/credits.txt
 * License.....: MIT
 */


typedef struct brainwallet_tmp
{
  u32 digest_buf[4];

} brainwallet_tmp_t;


KERNEL_FQ void m01337_init (KERN_ATTR_TMPS (brainwallet_tmp_t))
{
  
  /**
   * modifier
   */

  bool printout = false; 

  const u64 gid = get_global_id (0);

  if (gid >= GID_CNT) return;


  /**
   * base
   */


  const u32 pw_len = pws[gid].pw_len;

  u32 w[64] = { 0 };

  secp256k1_t preG; // need to change SECP256K1_TMPS_TYPE above to: PRIVATE_AS

  set_precomputed_basepoint_g (&preG);


  /**
   * loop
   */

  for (u32 i = 0, idx = 0; i < pw_len; i += 4, idx += 1)
  {
    w[idx] = pws[gid].i[idx];
  }


       char c4 = (w[0] >> 24) & 0xFF;
       char c3 = (w[0] >> 16) & 0xFF;
       char c2 = (w[0] >> 8) & 0xFF;
       char c1 = (w[0] & 0xFF);
       char c8 = (w[1] >> 24) & 0xFF;
       char c7 = (w[1] >> 16) & 0xFF;
       char c6 = (w[1] >> 8) & 0xFF;
       char c5 = (w[1] & 0xFF);
       char c12 = (w[2] >> 24) & 0xFF;
       char c11 = (w[2] >> 16) & 0xFF;
       char c10 = (w[2] >> 8) & 0xFF;
       char c9 = (w[2] & 0xFF);
       char c16 = (w[3] >> 24) & 0xFF;
       char c15 = (w[3] >> 16) & 0xFF;
       char c14 = (w[3] >> 8) & 0xFF;
       char c13 = (w[3] & 0xFF);
       char c20 = (w[4] >> 24) & 0xFF;
       char c19 = (w[4] >> 16) & 0xFF;
       char c18 = (w[4] >> 8) & 0xFF;
       char c17 = (w[4] & 0xFF);
       char c24 = (w[5] >> 24) & 0xFF;
       char c23 = (w[5] >> 16) & 0xFF;
       char c22 = (w[5] >> 8) & 0xFF;
       char c21 = (w[5] & 0xFF);
       char c28 = (w[6] >> 24) & 0xFF;
       char c27 = (w[6] >> 16) & 0xFF;
       char c26 = (w[6] >> 8) & 0xFF;
       char c25 = (w[6] & 0xFF);
       char c32 = (w[7] >> 24) & 0xFF;
       char c31 = (w[7] >> 16) & 0xFF;
       char c30 = (w[7] >> 8) & 0xFF;
       char c29 = (w[7] & 0xFF);
       char c36 = (w[8] >> 24) & 0xFF;
       char c35 = (w[8] >> 16) & 0xFF;
       char c34 = (w[8] >> 8) & 0xFF;
       char c33 = (w[8] & 0xFF);
       char c40 = (w[9] >> 24) & 0xFF;
       char c39 = (w[9] >> 16) & 0xFF;
       char c38 = (w[9] >> 8) & 0xFF;
       char c37 = (w[9] & 0xFF);

    if (printout)     {
      printf("pre-match for pw len %i is %c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c%c\n", 
           pw_len, 
           c1, c2, c3, c4, c5, c6, c7, c8, 
           c9, c10, c11, c12, c13, c14, c15, c16, 
           c17, c18, c19, c20, c21, c22, c23, c24, 
           c25, c26, c27, c28, c29, c30, c31, c32, 
           c33, c34, c35, c36, c37, c38, c39, c40);
     }

    
    
    //p.pw_len = apply_rules (rules_buf[il_pos].cmds, p.i, p.pw_len);


    //const u32 b = hc_swap32_S (p.i[0]);
    
    //printf("original input from a3:");
    //print_u32_array_as_chars(p.i, p.pw_len);
    //Take in the password and run it through sha256
    u32 sha_tmp[8];

    sha256_ctx_t ctx_sha;

    sha256_init (&ctx_sha);

    sha256_update_swap (&ctx_sha, w, pw_len);

    sha256_final (&ctx_sha);

    if (printout) {
    printf("sha1 results a0: ");
    print_u32_array_as_hex(ctx_sha.h, 8);
    }
    // convert password from b58 to binary
    u32 tmp[16] = { 0 };

    //const bool status_dec = b58dec_51 (tmp, ctx_sha.h);


    


    // verify sha256 (sha256 (tmp[0..37 - 4]))
    // real work is done in b58check where sha256 is run twice


    u32 prv_key[9]; // why is re-using the "tmp" variable here slower ?


    // prv_key[0] = (tmp[7] << 8) | (tmp[8] >> 24);
    // prv_key[1] = (tmp[6] << 8) | (tmp[7] >> 24);
    // prv_key[2] = (tmp[5] << 8) | (tmp[6] >> 24);
    // prv_key[3] = (tmp[4] << 8) | (tmp[5] >> 24);
    // prv_key[4] = (tmp[3] << 8) | (tmp[4] >> 24);
    // prv_key[5] = (tmp[2] << 8) | (tmp[3] >> 24);
    // prv_key[6] = (tmp[1] << 8) | (tmp[2] >> 24);
    // prv_key[7] = (tmp[0] << 8) | (tmp[1] >> 24);

    //Need to reverse the order
    prv_key[0] = ctx_sha.h[7];
    prv_key[1] = ctx_sha.h[6];
    prv_key[2] = ctx_sha.h[5];
    prv_key[3] = ctx_sha.h[4];
    prv_key[4] = ctx_sha.h[3];
    prv_key[5] = ctx_sha.h[2];
    prv_key[6] = ctx_sha.h[1];
    prv_key[7] = ctx_sha.h[0];

    //f("hashed pw: ");
   //print_u32_array_as_hex(prv_key, 8);


    if (printout) {
    printf("priv key: ");
    print_u32_array_as_hex(prv_key, 8);
    }

    // convert: pub_key = G * prv_key


    
    u32 x[8];
    u32 y[8];

    point_mul_xy (x, y, prv_key, &preG);


    // to public key:
     //printf("key x coordinate:");
   //  print_u32_array_as_hex(x,8);
//     printf("key y coordinate:");
   //  print_u32_array_as_hex(y,8);

    u32 pub_key[32] = { 0 };

    pub_key[16] =               (y[0] << 24);
    pub_key[15] = (y[0] >> 8) | (y[1] << 24);
    pub_key[14] = (y[1] >> 8) | (y[2] << 24);
    pub_key[13] = (y[2] >> 8) | (y[3] << 24);
    pub_key[12] = (y[3] >> 8) | (y[4] << 24);
    pub_key[11] = (y[4] >> 8) | (y[5] << 24);
    pub_key[10] = (y[5] >> 8) | (y[6] << 24);
    pub_key[ 9] = (y[6] >> 8) | (y[7] << 24);
    pub_key[ 8] = (y[7] >> 8) | (x[0] << 24);
    pub_key[ 7] = (x[0] >> 8) | (x[1] << 24);
    pub_key[ 6] = (x[1] >> 8) | (x[2] << 24);
    pub_key[ 5] = (x[2] >> 8) | (x[3] << 24);
    pub_key[ 4] = (x[3] >> 8) | (x[4] << 24);
    pub_key[ 3] = (x[4] >> 8) | (x[5] << 24);
    pub_key[ 2] = (x[5] >> 8) | (x[6] << 24);
    pub_key[ 1] = (x[6] >> 8) | (x[7] << 24);
    pub_key[ 0] = (x[7] >> 8) | (0x04000000);

  if (printout) {
    printf("pub key: ");
    
  print_u32_array_as_hex(pub_key, 17); }
    
    
    // calculate HASH160 for pub key

    sha256_ctx_t ctx;

    sha256_init   (&ctx);
    sha256_update (&ctx, pub_key, 65); // length of public key: 65
    sha256_final  (&ctx);


    // for (u32 i = 0; i < 8; i++) tmp[i] = ctx.h[i];

    // tmp[ 8] = 0; tmp[ 9] = 0; tmp[10] = 0; tmp[11] = 0;
    // tmp[12] = 0; tmp[13] = 0; tmp[14] = 0; tmp[15] = 0;

    // for (u32 i = 8; i < 16; i++) tmp[i] = 0;
    
    tmp[0] = ctx.h[0];
    tmp[1] = ctx.h[1];
    tmp[2] = ctx.h[2];
    tmp[3] = ctx.h[3];
    tmp[4] = ctx.h[4];
    tmp[5] = ctx.h[5];
    tmp[6] = ctx.h[6];
    tmp[7] = ctx.h[7];
    tmp[8] = 0;
    tmp[9] = 0;
    tmp[10] = 0;
    tmp[11] = 0;
    tmp[12] = 0;
    tmp[13] = 0;
    tmp[14] = 0;
    tmp[15] = 0;

    if (printout) {
      printf("SHA pt 2: ");
      print_u32_array_as_hex(tmp, 8); }


    // now let's do RIPEMD-160 on the sha256sum

    ripemd160_ctx_t rctx;

    ripemd160_init        (&rctx);
    ripemd160_update_swap (&rctx, tmp, 32);
    ripemd160_final       (&rctx);

    const u32 r0 = rctx.h[0];
    const u32 r1 = rctx.h[1];
    const u32 r2 = rctx.h[2];
    const u32 r3 = rctx.h[3];

  if (printout) {
    printf("ripmd out: ");
    print_u32_array_as_hex(rctx.h, 5); 
  }

      
   tmps[gid].digest_buf[0] = r0;
   tmps[gid].digest_buf[1] = r1;
   tmps[gid].digest_buf[2] = r2;
   tmps[gid].digest_buf[3] = r3;
  
}
    


KERNEL_FQ void m01337_loop (KERN_ATTR_TMPS (brainwallet_tmp_t))
{
  return;
}

KERNEL_FQ void m01337_comp (KERN_ATTR_TMPS (brainwallet_tmp_t))
{
  /**
   * modifier
   */

  const u64 gid = get_global_id (0);

  if (gid >= GID_CNT){
    return;
  }

  //const u64 lid = get_local_id (0);

  /**
   * digest
   */

  const u32 r0 = tmps[gid].digest_buf[DGST_R0];
  const u32 r1 = tmps[gid].digest_buf[DGST_R1];
  const u32 r2 = tmps[gid].digest_buf[DGST_R2];
  const u32 r3 = tmps[gid].digest_buf[DGST_R3];

  #define il_pos 0

  u32 digest_tp[4];

digest_tp[0] = r0;
digest_tp[1] = r1;
digest_tp[2] = r2;
digest_tp[3] = r3;
//printf("comp-m pre - %u %u %u %u  is  %i \n", digest_tp[0], digest_tp[1] , digest_tp[2] , digest_tp[3]);
if (check (digest_tp,
             bitmaps_buf_s1_a,
             bitmaps_buf_s1_b,
             bitmaps_buf_s1_c,
             bitmaps_buf_s1_d,
             bitmaps_buf_s2_a,
             bitmaps_buf_s2_b,
             bitmaps_buf_s2_c,
             bitmaps_buf_s2_d,
             BITMAP_MASK,
             BITMAP_SHIFT1,
             BITMAP_SHIFT2))
{
  int digest_pos = find_hash (digest_tp, DIGESTS_CNT, &digests_buf[DIGESTS_OFFSET_HOST]);
  //  printf("comp-m - %u %u %u %u  is  %i \n", digest_tp[0], digest_tp[1] , digest_tp[2] , digest_tp[3],digest_pos);

  if (digest_pos != -1)
  {
    const u32 final_hash_pos = DIGESTS_OFFSET_HOST + digest_pos;
 // printf("hashes_shown pointer %p", &hashes_shown[final_hash_pos]);
    //u32 b = hc_atomic_nop (&hashes_shown[final_hash_pos]);
    u32 a = hc_atomic_inc (&hashes_shown[final_hash_pos]);
  // printf("atomic thing for position %i is %u, final pos is %u \n", digest_pos, a, final_hash_pos);

    
    mark_hash (plains_buf, d_return_buf, SALT_POS_HOST, DIGESTS_CNT, digest_pos, final_hash_pos, gid, il_pos, 0, 0);
  }
}

}
