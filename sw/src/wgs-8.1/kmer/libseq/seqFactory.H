#ifndef SEQFACTORY_H
#define SEQFACTORY_H

#include "util.h"
#include "seqFile.H"

class seqFactory {
protected:
  seqFactory();
  ~seqFactory();

public:
  static seqFactory *instance(void) {
    if (me == 0L)
      me = new seqFactory;
    return(me);
  };

  void           registerFile(seqFile   *f);
  seqFile       *openFile(const char *name);
private:
  static seqFactory  *me;

  u32bit         _filesNum;
  u32bit         _filesMax;
  seqFile      **_files;
};


#define openSeqFile(S)    seqFactory::instance()->openFile((S))


#endif  //  SEQFACTORY_H
