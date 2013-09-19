/* unset_var.c 1.02 (C) Richard K. Lloyd 2013 <rklloyd@gmail.com>

   LD_PRELOAD code to save LD_LIBRARY_PATH, blank LD_LIBRARY_PATH
   if the file to be exec'd isn't a full path, run the original
   exec*() library routine and then restore LD_LIBRARY_PATH.

   This way, we can avoid Fedora 15 libraries being picked up
   by helper apps or plugins that are subsequently loaded by
   Google Chrome.

   strings -a /opt/google/chrome/chrome | grep ^exec
   reveals three exec* routines used by the binary:
   execvp(), execve() and execlp().

   Compile with:
   gcc -O -fpic -shared -s -o unset_var.so unset_var.c -ldl

   Run with:
   export LD_PRELOAD=/path/to/unset_var.so
   /opt/google/chrome/google-chrome
*/

/* Have to build with this flag defined */
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

/* The environmental variable we're going to unsetenv() */
#define ENV_VAR "LD_LIBRARY_PATH"

/* Some system headers */
#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <stdarg.h>
#include <string.h>

/* Each routine we intercept is likely to have different parameter types
   and return types too, so firstly, we create common code macros */

/* Define local variables for function, passing in the function return type */
#define INTERCEPT_LOCAL_VARS(return_type) \
   char *envptr=getenv(ENV_VAR); \
   static char savebuf[BUFSIZ]; \
   /* FILE *outhand=fopen("/tmp/exec.log","a"); */ \
   return_type retval

/* Save ENV_VAR value in local buffer and then unset it
   if it's not a full path */
#define INTERCEPT_SAVE_VAR(fname) \
   if (envptr!=(char *)NULL && envptr[0]!='\0') \
      (void)snprintf(savebuf,BUFSIZ,ENV_VAR "=%s",envptr); \
   else savebuf[0]='\0'; \
   /* if (outhand!=(FILE *)NULL) { fprintf(outhand,"%s\n",fname); (void)fclose(outhand); } */ \
   if (strstr(fname,"/")==(char *)NULL || \
       strstr(fname,"/opt/google/talkplugin/")!=(char *)NULL) unsetenv(ENV_VAR)

/* Restore ENV_VAR value and return value from function. */
#define INTERCEPT_RESTORE_VAR \
   if (savebuf[0]) putenv(savebuf); else unsetenv(ENV_VAR); \
   return(retval)

/* Now string it into macros for different numbers of parameters. */

/* execvp() */
#define INTERCEPT_2_PARAMS(return_type,function_name,function_name_str,param_1_type,param_1_name,param_2_type,param_2_name) \
return_type function_name(param_1_type param_1_name,param_2_type param_2_name) \
{ \
   INTERCEPT_LOCAL_VARS(return_type); \
   return_type (*original_##function_name)(param_1_type,param_2_type); \
   original_##function_name=dlsym(RTLD_NEXT,function_name_str); \
   INTERCEPT_SAVE_VAR(param_1_name); \
   retval=(*original_##function_name)(param_1_name,param_2_name); \
   INTERCEPT_RESTORE_VAR; \
}

/* execve() */
#define INTERCEPT_3_PARAMS(return_type,function_name,function_name_str,param_1_type,param_1_name,param_2_type,param_2_name,param_3_type,param_3_name) \
return_type function_name(param_1_type param_1_name,param_2_type param_2_name,param_3_type param_3_name) \
{ \
   INTERCEPT_LOCAL_VARS(return_type); \
   return_type (*original_##function_name)(param_1_type,param_2_type,param_3_type); \
   original_##function_name=dlsym(RTLD_NEXT,function_name_str); \
   INTERCEPT_SAVE_VAR(param_1_name); \
   retval=(*original_##function_name)(param_1_name,param_2_name,param_3_name); \
   INTERCEPT_RESTORE_VAR; \
}

/* execlp() - I'm not fully sure I've done the va_list stuff right here! */
#define INTERCEPT_2_VARARGS(return_type,function_name,function_name_str,param_1_type,param_1_name,param_2_type,param_2_name) \
return_type function_name(param_1_type param_1_name,param_2_type param_2_name,...) \
{ \
   va_list args; \
   INTERCEPT_LOCAL_VARS(return_type); \
   return_type (*original_##function_name)(param_1_type,param_2_type,...); \
   original_##function_name=dlsym(RTLD_NEXT,function_name_str); \
   INTERCEPT_SAVE_VAR(param_1_name); \
   va_start(args,param_2_name); \
   retval=(*original_##function_name)(param_1_name,param_2_name,args); \
   va_end(args); \
   INTERCEPT_RESTORE_VAR; \
}

/* Only 3 routines intercepted so far - may be more in the future */
INTERCEPT_2_PARAMS(int,execvp,"execvp",const char *,file,const char **,argv);
INTERCEPT_3_PARAMS(int,execve,"execve",const char *,filename,const char **,argv,const char **,envp);
INTERCEPT_2_VARARGS(int,execlp,"execlp",const char *,file,const char *,arg);
