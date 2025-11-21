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

typedef struct brainwallet_tmp
{
  u32 digest_buf[4];

} brainwallet_tmp_t;


KERNEL_FQ void m01337_init (KERN_ATTR_TMPS (brainwallet_tmp_t))
{
  const u64 gid = get_global_id (0);

  if (gid >= GID_CNT) return;


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


    u32 prv_key[9];

    prv_key[0] = ctx_sha.h[7];
    prv_key[1] = ctx_sha.h[6];
    prv_key[2] = ctx_sha.h[5];
    prv_key[3] = ctx_sha.h[4];
    prv_key[4] = ctx_sha.h[3];
    prv_key[5] = ctx_sha.h[2];
    prv_key[6] = ctx_sha.h[1];
    prv_key[7] = ctx_sha.h[0];

    u32 x[8];
    u32 y[8];

    point_mul_xy (x, y, prv_key, &preG);

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

    sha256_ctx_t ctx;

    sha256_init   (&ctx);
    sha256_update (&ctx, pub_key, 65);
    sha256_final  (&ctx);

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

    ripemd160_ctx_t rctx;

    ripemd160_init        (&rctx);
    ripemd160_update_swap (&rctx, tmp, 32);
    ripemd160_final       (&rctx);

    const u32 r0 = rctx.h[0];
    const u32 r1 = rctx.h[1];
    const u32 r2 = rctx.h[2];
    const u32 r3 = rctx.h[3];

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

  if (digest_pos != -1)
  {
    const u32 final_hash_pos = DIGESTS_OFFSET_HOST + digest_pos;

    u32 a = hc_atomic_inc (&hashes_shown[final_hash_pos]);

    
    mark_hash (plains_buf, d_return_buf, SALT_POS_HOST, DIGESTS_CNT, digest_pos, final_hash_pos, gid, il_pos, 0, 0);
  }
}

}
