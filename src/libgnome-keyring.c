/* missing_functions.c 3.00 (C) Richard K. Lloyd 2015 <rklloyd@gmail.com>

   Provides a gnome_keyring_attribute_list_new() function (was
   a macro in CentOS 6 causing a missing symbol error when Google Chrome
   was started up) that's present in later libgnome-keyring libraries.
   See: https://mail.gnome.org/archives/commits-list/2012-January/msg08007.html
*/

/* Providing the "missing" gnome_keyring_attribute_list_new function
   -----------------------------------------------------------------
   To avoid having to install various *-devel packages, the required
   definitions in CentOS 6.6 headers have been simplified to avoid the
   need for any include files. I have also added the string "Custom" to the end
   of any definitions that may clash with the original CentOS 6 libraries.
*/

/* Simplifying glib/gtypes.h, glib/garray.h and gnome-keyring.h,
   we get this: */
struct GnomeKeyringAttributeListCustom
{
  char *data;
  int len;
};

/* Simplifying glib/gtypes.h and glib/garray.h, we get this: */
struct GnomeKeyringAttributeListCustom *
g_array_new (int zero_terminated, int clear_, unsigned int element_size);

/* This is straight from gnome-keyring.h: */
typedef enum {
        GNOME_KEYRING_ATTRIBUTE_TYPE_STRING,
        GNOME_KEYRING_ATTRIBUTE_TYPE_UINT32
} GnomeKeyringAttributeTypeCustom;

/* Simplifying glib/gtypes.h and gnome-keyring.h, we get this: */
typedef struct {
        char *name;
        GnomeKeyringAttributeTypeCustom type;
        union {
                char *string;
                unsigned int integer;
        } value;
} GnomeKeyringAttributeCustom;

/* The "missing" function from CentOS 6's gnome-keyring library */
struct GnomeKeyringAttributeListCustom *
gnome_keyring_attribute_list_new (void)
{
   return g_array_new (0, 0, sizeof (GnomeKeyringAttributeCustom));
}
